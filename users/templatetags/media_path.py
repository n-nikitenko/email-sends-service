from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape

from config.settings import MEDIA_URL

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def media_path(src, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return f"{MEDIA_URL}{esc(src)}"
