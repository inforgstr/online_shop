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
    fields = ["name", "img"]


@admin.register(shop_models.Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number"]


@admin.register(shop_models.CartItem)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "size", "quantity"]


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
    list_filter = ["type", "style", "timestamp", "stars"]
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
        "sizes",
        "img1",
        "img2",
        "img3",
    ]
    search_fields = ["title"]


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


class OrderItemInline(admin.TabularInline):
    model = shop_models.OrderItem
    raw_id_fields = ["product"]


@admin.register(shop_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = [
        "paid",
        "created",
        "updated",
    ]
    inlines = [OrderItemInline]
