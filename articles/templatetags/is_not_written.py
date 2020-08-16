from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_not_written(value):
    return True if value.publish_at is None else False
