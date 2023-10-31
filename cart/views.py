from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

from shop.models import Product
from shop.forms import ProductCartForm
from cart.cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def remove_all_cart(request):
    if request.method == "POST":
        cart = Cart(request)
        cart.clear()
    return redirect(reverse("cart:cart_detail"))


@require_POST
def add_cart(request, product_slug):
    """
    View for add or create a new cart item with form.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)

    form = ProductCartForm(product=product, data=request.POST)
    if form.is_valid() and product.is_available:
        cd = form.cleaned_data

        added = cart.add(product, cd["quantity"], cd["sizes"])
        if added:
            messages.success(request, "Product added to your cart!")
    else:
        messages.error(request, "Product is not available!")
    return redirect(product.get_absolute_url())


def change_cart_sub_manage(request, product_slug, size_name):
    """
    View for substract cart's product quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    if product.is_available:
        cart.add(product, -1, size_name)
    return redirect(reverse("cart:cart_detail"))


def change_cart_add_manage(request, product_slug, size_name):
    """
    View for add cart's product quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    if product.is_available:
        cart.add(product, 1, size_name)
    return redirect(reverse("cart:cart_detail"))


def remove_cart(request, product_slug, size_name):
    """
    View for removing item from user cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    if product.is_available:
        cart.remove(product, size_name)
    return redirect(reverse("cart:cart_detail"))
