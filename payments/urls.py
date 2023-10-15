from django.urls import path

from payments import views


app_name = "payments"

urlpatterns = [
    path("product_page/", views.product_page, name="product_page"),
    path("payment_successfull/", views.payment_successfull, name="payment_successfull"),
    path("payment_cancelled/", views.payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook/", views.stripe_webhook, name="stripe_webhook"),
]