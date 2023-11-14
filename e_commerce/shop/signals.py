import os

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from better_profanity import profanity
from django.contrib.auth.models import User

from shop.models import Review, ShopBrand, Product, ProductStyle, Profile


@receiver(post_save, sender=User)
def create_new_user_on_save(sender, instance: User, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def profile_auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False

    new_file = instance.image
    if old_file and old_file != new_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)


@receiver(post_delete, sender=Profile)
def profile_auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=User)
def delete_user_on_delete(sender, instance, *args, **kwargs):
    user = Profile.objects.filter(user=instance)
    user.delete()


@receiver(post_save, sender=Review)
def set_product_stars(sender, instance: Review, created, **kwargs):
    if created:
        body = profanity.censor(instance.body)
        if instance.body != body:
            instance.body = body
            instance.save()

        product_reviews = instance.product.product_reviews.all()
        product = instance.product
        if product_reviews:
            avg_stars = round(
                sum(x.stars for x in product_reviews) / len(product_reviews), 1
            )
            if product.stars != avg_stars:
                product.stars = avg_stars
                product.save()


@receiver(post_delete, sender=Review)
def pop_product_stars(sender, instance: Review, *args, **kwrags):
    product_reviews = instance.product.product_reviews.exclude(id=instance.id)
    product = instance.product
    if product_reviews:
        avg_stars = round(
            sum(x.stars for x in product_reviews) / len(product_reviews),
            1,
        )
        if avg_stars != product.stars:
            product.stars = avg_stars
            product.save()
    else:
        product.stars = None
        product.save()


@receiver(post_delete, sender=ShopBrand)
def brand_auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img and os.path.isfile(instance.img.path):
        os.remove(instance.img.path)


@receiver(post_delete, sender=ProductStyle)
def product_brand_auto_delete(sender, instance, **kwargs):
    if instance.img and os.path.isfile(instance.img.path):
        os.remove(instance.img.path)


@receiver(post_delete, sender=Product)
def product_auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img1 and os.path.isfile(instance.img1.path):
        os.remove(instance.img1.path)
    if instance.img2 and instance.img3:
        if os.path.isfile(instance.img2.path):
            os.remove(instance.img2.path)
        if os.path.isfile(instance.img3.path):
            os.remove(instance.img3.path)


@receiver(pre_save, sender=ShopBrand)
def brand_auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ShopBrand.objects.get(pk=instance.pk).img
    except ShopBrand.DoesNotExist:
        return False

    new_file = instance.img
    if old_file != new_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)


@receiver(pre_save, sender=ProductStyle)
def product_brand_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ProductStyle.objects.get(pk=instance.pk).img
    except ProductStyle.DoesNotExist:
        return False

    new_file = instance.img
    if old_file != new_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)


@receiver(post_save, sender=Product)
def set_available_on_create(sender, instance, created, **kwargs):
    if created:
        if instance.quantity == 0:
            instance.is_available = False
        elif instance.quantity > 0:
            instance.is_available = True
        instance.save()


@receiver(pre_save, sender=Product)
def product_auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    if instance.quantity == 0:
        instance.is_available = False
    elif instance.quantity > 0:
        instance.is_available = True

    try:
        old_file = Product.objects.get(pk=instance.pk)
        old_file2 = old_file.img2
        old_file3 = old_file.img3
    except Product.DoesNotExist:
        return False

    new_file = instance.img1
    new_file2 = instance.img2
    new_file3 = instance.img3

    if old_file.img1 != new_file and os.path.isfile(old_file.img1.path):
        os.remove(old_file.img1.path)

    if old_file2 and old_file3:
        if old_file2 != new_file2 and os.path.isfile(old_file2.path):
            os.remove(old_file2.path)

        if old_file3 != new_file3 and os.path.isfile(old_file3.path):
            os.remove(old_file3.path)
