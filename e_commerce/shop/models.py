from django.db import models
from django.core.validators import MaxValueValidator
from ckeditor.fields import RichTextField

from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from shop.utils import rand_slug


class Profile(models.Model):
    image = models.ImageField(upload_to="profiles/img/%Y/%m/%d/", blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.phone_number}"

    def get_total_price(self):
        return sum(
            int(query.quantity) * float(query.product.get_discounted_price())
            for query in self.user.user_carts.all()
        )


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_carts"
    )
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="product_carts",
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(
        "shop.Size", on_delete=models.CASCADE, related_name="size_carts", blank=True
    )

    def __str__(self) -> str:
        return "%s - %s" % (self.user.email, self.product.title)

    def get_price(self):
        return self.product.get_discounted_price()


class ShopBrand(models.Model):
    """
    Shop Brands model.
    """

    name = models.CharField("Brand Name", max_length=150)
    img = models.FileField("Brand Image (*.svg)", upload_to="brands/")

    def __str__(self) -> str:
        return "%s" % (self.name)


class Shop(models.Model):
    """
    Shop model.
    Overview of shop - landing page.
    """

    name = models.CharField(max_length=150)
    brands = models.IntegerField("International Brands")
    quality = models.IntegerField("High-Quality Products")
    customers = models.IntegerField("Happy customers")
    about = RichTextField("About page content")

    # social media links
    twitter = models.URLField()
    facebook = models.URLField()
    instagram = models.URLField()

    def __str__(self) -> str:
        return "%s" % (self.name)


class Size(models.Model):
    """
    Product sizes model.
    """

    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return "%s" % (self.name)


class ProductBrand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class ProductStyle(models.Model):
    img = models.ImageField(upload_to="product_brands/")
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class PopularProductManager(models.Manager):
    def get_queryset(self):
        popular_products = (
            Product.objects.annotate(
                orders_count=models.Count("product_orders"),
                reviews_count=models.Count("product_reviews"),
            )
            .order_by("-timestamp")
            .order_by("-reviews_count")
            .order_by("-stars")
            .order_by("-orders_count")
            .filter(orders_count__gte=1)
        )
        return popular_products


class Product(models.Model):
    class ProductGender(models.TextChoices):
        MAN = "M", "Man"
        WOMAN = "WM", "Woman"
        MULTIPLE = "ML", "Multiple"

    slug = models.SlugField(blank=True, editable=False)
    title = models.CharField(max_length=140)
    brand = models.ForeignKey(
        ProductBrand, on_delete=models.CASCADE, related_name="brand_products"
    )
    type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="type_products"
    )
    style = models.ManyToManyField(ProductStyle, related_name="styles_products")

    img1 = models.ImageField(upload_to="products/img1/")
    img2 = models.ImageField(upload_to="products/img2/", null=True, blank=True)
    img3 = models.ImageField(upload_to="products/img3/", null=True, blank=True)

    quantity = models.PositiveIntegerField()
    gender = models.CharField(
        "Product Gender", choices=ProductGender.choices, default=ProductGender.MULTIPLE
    )
    stars = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    price = models.DecimalField("Current Price", max_digits=20, decimal_places=2)
    discount = models.PositiveIntegerField(
        default=0,
        verbose_name="Price Discount (%)",
        validators=[MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    is_available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(
        "shop.Size", related_name="size_products", blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    description = RichTextField()

    objects = models.Manager()
    populars = PopularProductManager()

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
        ]

    @property
    def image1_url(self):
        if self.img1 and hasattr(self.img1, "url"):
            return self.img1.url

    @property
    def image2_url(self):
        if self.img2 and hasattr(self.img2, "url"):
            return self.img2.url

    @property
    def image3_url(self):
        if self.img3 and hasattr(self.img3, "url"):
            return self.img3.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug(self.title)
        super().save(*args, **kwargs)

    def _check_cart(self, user, size_obj):
        try:
            user_cart = CartItem.objects.get(product=self, user=user, size=size_obj)
            return user_cart
        except CartItem.DoesNotExist:
            return False

    def add_cart(self, user, size, quantity):
        try:
            size = Size.objects.get(name=size)
        except Size.DoesNotExist:
            return False

        user_cart = self._check_cart(user, size)
        if user_cart and (
            (int(user_cart.quantity) < int(self.quantity) and int(quantity) > 0)
            or (
                int(user_cart.quantity) <= int(self.quantity)
                and int(quantity) < 0
                and int(user_cart.quantity) > 1
            )
        ):
            user_cart.quantity += int(quantity)
            user_cart.save()
            return True
        elif not user_cart:
            CartItem.objects.create(
                user=user, product=self, quantity=quantity, size=size
            )
            return True
        return False

    def remove_cart(self, user, size):
        try:
            size = Size.objects.get(name=size)
        except Size.DoesNotExist:
            return False

        user_cart = self._check_cart(user, size)
        if user_cart:
            user_cart.delete()
            return True
        return False

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    def refresh_quantity(self, amount):
        """
        Save quantity into database.
        """
        if amount > self.quantity:
            return False
        self.quantity -= amount
        super().save()

    def get_discounted_price(self):
        if self.discount:
            discount = 100 - self.discount
            return round(discount / 100 * float(self.price), 2)
        return self.price

    def __str__(self) -> str:
        return "%s" % (self.title)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    stars = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reviews"
    )
    body = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-posted_date"]),
        ]

    def __str__(self) -> str:
        return "%s" % (self.user.email)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_orders"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.first_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="product_orders", on_delete=models.CASCADE
    )
    size = models.ForeignKey(Size, related_name="size_orders", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.first_name} - {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
