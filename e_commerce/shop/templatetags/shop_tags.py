from django import template


register = template.Library()


@register.filter("make_int")
def remove_zero(value):
    result = value
    if str(value).endswith("0"):
        result = int(value)
    return result
