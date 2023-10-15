from django.db import models

from shop.models import UserProfile


class UserPayment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_payments"
    )
    completed = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.user.email
