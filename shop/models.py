from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class UserWishlist(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_wishlist"
    )
    product = models.ForeignKey(
        "shop.Product", on_delete=models.CASCADE, related_name="product_wishlist"
    )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return "%s - %s" % (self.user.email, self.product.title)


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
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


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
    size = models.ManyToManyField("shop.Size", related_name="size_products", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    objects = models.Manager()

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
        ]

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     kwargs = {
    #         "pk": self.pk,
    #         "slug": self.slug,
    #     }
    #     return reverse("shop:product-detail", kwargs=kwargs)

    def get_stars(self):
        rate = self.stars - int(self.stars)
        if rate > 0:
            return [x for x in range(int(self.stars))] + ["/"]
        return range(int(self.stars))

    def refresh_quantity(self, amount):
        """
        Save quantity into database.
        """
        if amount > self.quantity:
            return False
        self.quantity -= amount
        super().save()

    def check_availablity(self, quantity):
        """
        Checks for product quantity.
        If product does not exist it will save as is_available = False
        """
        if self.quantity == 0:
            self.is_available = False
            super().save()

    def get_discounted_price(self):
        if self.discount:
            discount = 100 - self.discount
            return round(discount / 100 * float(self.price), 2)
        return False

    def __str__(self) -> str:
        return "%s" % (self.title)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    stars = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_reviews"
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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_orders"
    )
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_orders"
    )
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s - %s" % (self.user.email, self.product.title)
