from django.contrib import admin

from payments.models import UserPayment


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "completed", "stripe_checkout_id"]
