from django.urls import path

from shop import views


app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_page, name="about"),
    path(
        "product/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
        "product/<slug:product_slug>/write-review/",
        views.product_detail_review,
        name="product_detail_review",
    ),
    path("brands/", views.brand_list, name="brand_list"),
    path("product-filter/", views.product_filter, name="product_filter"),
    path("orders/create-order/", views.order_create, name="order_create"),
]
