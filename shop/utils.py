import random
import string

from django.utils.text import slugify


def rand_slug(text):
    return slugify(text, allow_unicode=True) + "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
