from django.db import models
from django.db.models import Q

from core.additional.models import CoreModel


class TagQuerySet(models.QuerySet):

    def all(self):
        return self.filter(is_active=True)

    def search(self, query):
        lookup = (
            Q(is_active=True) &
            Q(name__icontains=query)
        )
        return self.filter(lookup)


class TagManager(models.Manager):

    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Tag(CoreModel):
    """
    A model for tagging an article.

    Attributes:
        name (CharField): the name of tag
    """
    name = models.CharField(max_length=100)

    objects = TagManager()

    class Meta:
        """
        Attributes:
            ordering (List): use to determine the ordering of model objects when listed
        """
        ordering = ['-timestamp', '-updated', ]

    def __str__(self):
        return self.name
