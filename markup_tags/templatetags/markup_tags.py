from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def smallcaps(string):
    if string.isupper():
        return mark_safe('<span style="font-variant: small-caps;">%s</span>' %
                         string.title())
    else:
        return string
