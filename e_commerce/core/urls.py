from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls", namespace="shop")),
    path("user/", include("cart.urls", namespace="cart")),
    path("payment/", include("payments.urls", namespace="payments")),
    path("auth-shop/", include("auth.urls", namespace="auth")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "SHOP CO"
