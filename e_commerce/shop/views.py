from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from cart.cart import Cart
from shop.tasks import order_delay

from shop.models import (
    Product,
    ShopBrand,
    ProductStyle,
    Review,
    ProductBrand,
    OrderItem,
    Size,
)
from shop.forms import (
    NewsletterForm,
    ProductCartForm,
    ProductReviewForm,
    ProductFilterForm,
    OrderCreateForm,
)


def home(request):
    arrivals = Product.objects.all()[:4]
    brands = ShopBrand.objects.all()
    popular_products = Product.populars.all()[:4]
    styles = ProductStyle.objects.all()
    happy_reviews = Review.objects.filter(stars__gte=4).order_by("-stars")[:12]

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data["email"]
            send_mail(
                "SHOP.CO: subsriber!",
                "Hi, there! You have subscribed to our Newsletter!",
                settings.EMAIL_HOST_USER,
                [to],
            )
            if "is_subs" in request.session:
                request.session["is_subs"] = True
            messages.success(
                request,
                f"Success! We will contact with you.",
            )
        else:
            messages.error(request, "Please, enter a valid email address.")

        return redirect(reverse("shop:home"))

    return render(
        request,
        "shop/index.html",
        {
            "arrivals": arrivals,
            "brands": brands,
            "popular_products": popular_products,
            "styles": styles,
            "reviews": happy_reviews,
        },
    )


def about_page(request):
    return render(request, "shop/about.html")


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    product_styles = product.style.values_list("id", flat=True)
    similar_products = Product.objects.filter(style__in=product_styles).exclude(
        pk=product.pk
    )
    similar_products = similar_products.annotate(same_styles=Count("style")).order_by(
        "-same_styles"
    )[:4]
    form = ProductCartForm(product=product, data={"quantity": 1})

    context = {
        "product": product,
        "form": form,
        "similars": similar_products,
    }
    if request.GET.get("type") == "reviews":
        context["reviews"] = (
            product.product_reviews.all().order_by("-posted_date")
            if product.product_reviews.all()
            else "empty"
        )

    return render(request, "shop/detail.html", context)


@login_required
def product_detail_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    form = ProductReviewForm()

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.stars = form.cleaned_data["rating"]
            review.user = request.user
            review.save()
            messages.success(
                request,
                "Your review has successfully added to product reviews. Thank you for your review!",
            )
        else:
            messages.error(request, "Please create your review again with valid data!")
        return redirect(str(product.get_absolute_url()) + "?type=reviews")

    return render(
        request,
        "shop/product_review.html",
        {"form": form, "product": product, "reviews": product.product_reviews.all()},
    )


def product_filter(request):
    params = request.GET
    q = params.get("q")
    p_brand = params.get("brand")
    p_style = params.get("style")
    p_type = params.get("type")
    gender = params.get("gender")
    filter_by = params.get("filter_by")
    min = params.get("min_price")
    max = params.get("max_price")

    form = ProductFilterForm()

    products = Product.objects.all()
    if q:
        search_vector = SearchVector("title", weight="A") + SearchVector(
            "description", weight="B"
        )
        search_query = SearchQuery(q)
        products = (
            Product.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
    if p_style or p_type or gender or p_brand or filter_by:
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            if filter_by:
                if filter_by == "MO":
                    products = products.annotate(orders=Count("product_orders")).filter(
                        orders__gte=1
                    )
                elif filter_by == "NA":
                    products = products.order_by("-timestamp")
                elif filter_by == "MP":
                    products = products.annotate(
                        reviews_count=Count("product_reviews")
                    ).filter(reviews_count__gte=1, stars__gte=4)
            if max:
                products = products.filter(price__lte=max)
            if min:
                products = products.filter(price__gte=min)
            if gender and gender != "ML":
                products = products.filter(Q(gender=gender) | Q(gender="ML"))
            if p_brand:
                products = products.filter(brand__name=p_brand)
            if p_style:
                try:
                    style = ProductStyle.objects.get(name=p_style)
                    products = products.filter(style__in=[style.pk])
                except ProductStyle.DoesNotExist:
                    products = []
            if p_type:
                products = products.filter(type__name=p_type)

    return render(
        request,
        "shop/filter_page.html",
        {
            "products": products,
            "q": q,
            "form": form,
        },
    )


def brand_list(request):
    brands = ProductBrand.objects.all()
    return render(request, "shop/product_brands.html", {"brands": brands})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                product = get_object_or_404(Product, pk=item["product"]["pk"])
                size = get_object_or_404(Size, name=item["size"])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item["price"],
                    quantity=item["quantity"],
                    size=size,
                )
            cart.clear()
            order_delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse("payments:process"))

    else:
        form = OrderCreateForm(instance=request.user)
    return render(request, "order/create.html", {"form": form})
