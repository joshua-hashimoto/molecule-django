from uuid import uuid4

from django.db import models


class CoreModel(models.Model):
    """
    A model for all app models.

    Attributes:
        timestamp (DateTimeField): the date that the data was saved. auto_now_add will save only once.
        updated (DateTimeField): the date that the data was updated.
            auto_now will auto update the data every time the object updated.
        is_active (BooleanField): whither if the object is 'active' or not. defaults to True.

    Note:
        by setting Meta class's abstract attribute to True,
        django will not make a table for this model.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
