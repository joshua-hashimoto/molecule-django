from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_not_published(value):
    if value.publish_at is None:
        return not value.publish_at
    return value.publish_at > timezone.now()
