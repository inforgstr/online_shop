from django.urls import path

from payments import views


app_name = "payments"

urlpatterns = [
    path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("webhook/", views.stripe_webhook, name="stripe-webhook"),
    path("remove-orders/", views.payment_orders_clear, name="payment_order_clear"),
]
