from django.shortcuts import render
from django.db.models import Count

from shop.models import Product, ShopBrand, Shop, ProductStyle, Review


def home(request):
    arrivals = Product.objects.all()[:4]
    brands = ShopBrand.objects.all()
    shop = Shop.objects.last()
    popular_products = Product.populars.all()[:4]
    styles = ProductStyle.objects.all()
    happy_reviews = Review.objects.filter(stars__gte=4)

    context = {
        "arrivals": arrivals,
        "brands": brands,
        "shop": shop,
        "popular_products": popular_products,
        "styles": styles,
        "reviews": happy_reviews,
    }
    return render(request, "shop/index.html", context)
