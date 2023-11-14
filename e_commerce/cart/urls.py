from django.urls import path

from cart import views


app_name = "cart"

urlpatterns = [
    path("add-cart/<slug:product_slug>/", views.add_cart, name="add_cart"),
    path(
        "manage-add-cart/<slug:product_slug>/<str:size_name>/",
        views.change_cart_add_manage,
        name="cart_add_manage",
    ),
    path(
        "manage-sub-cart/<slug:product_slug>/<str:size_name>/",
        views.change_cart_sub_manage,
        name="cart_sub_manage",
    ),
    path(
        "remove-cart-post/<slug:product_slug>/<str:size_name>/",
        views.remove_cart,
        name="remove_cart",
    ),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/remove-all/", views.remove_all_cart, name="remove_all_cart"),
]
