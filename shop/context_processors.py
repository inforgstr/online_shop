from django.utils import timezone

from shop.models import Shop
from shop.forms import NewsletterForm


def shop(request):
    is_subs = request.session.get("is_subs")
    return {
        "shop": Shop.objects.last(),
        "year": timezone.now().year,
        "is_subs": is_subs,
    }


def shop_form(request):
    return {"n_form": NewsletterForm()}
