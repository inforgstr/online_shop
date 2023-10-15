from django.dispatch import receiver
from django.db.models.signals import post_save

from payments.models import UserPayment
from shop.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(user=instance)
