from django.shortcuts import render
from django.db.models import Count

from shop.models import Product, ShopBrand, Shop


def home(request):
    arrivals = Product.objects.all()[:4]
    brands = ShopBrand.objects.all()
    shop = Shop.objects.last()
    popular_products = (
        Product.objects.annotate(
            orders_count=Count("product_orders"), reviews_count=Count("product_reviews")
        )
        .order_by("-timestamp")
        .order_by("-reviews_count")
        .order_by("-stars")
        .order_by("-orders_count")
        .filter(orders_count__gte=1)
    )[:4]

    context = {
        "arrivals": arrivals,
        "brands": brands,
        "shop": shop,
        "popular_products": popular_products,
    }
    return render(request, "shop/index.html", context)
