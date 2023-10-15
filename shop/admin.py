from django.contrib import admin

from shop import models as shop_models


@admin.register(shop_models.ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(shop_models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(shop_models.ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(shop_models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "is_staff", "is_superuser", "date_joined"]
    list_filter = ["email", "is_staff"]
    search_fields = ["email"]


@admin.register(shop_models.UserWishlist)
class UserWishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]


@admin.register(shop_models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "title",
        "gender",
        "slug",
        "brand",
        "stars",
        "price",
        "discount",
        "published",
        "is_available",
    ]
    list_filter = ["title", "timestamp", "stars"]
    fields = [
        "type",
        "title",
        "gender",
        "brand",
        "style",
        "description",
        "quantity",
        "price",
        "discount",
        "is_available",
        "published",
        "size",
        "img1",
        "img2",
        "img3",
    ]


@admin.register(shop_models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(shop_models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "stars",
        "posted_date",
    ]


@admin.register(shop_models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(shop_models.ShopBrand)
class ShopBrandAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(shop_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "quantity",
        "order_date",
    ]
    list_filter = [
        "user",
        "product",
        "quantity",
        "order_date",
    ]
