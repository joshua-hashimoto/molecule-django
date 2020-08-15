from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown

from core.additional.models import CoreModel
from articles.models import Article


class CommentQuerySet(models.QuerySet):
    """
    custom QuerySet for model Comment
    """

    def all(self):
        """
        Returns:
            queryset: return all object with is_active=True
        """
        queryset = self.filter(is_active=True)
        return queryset


class CommentManager(models.Manager):
    """
    custom manager for model Comment using CommentManager
    """

    def get_queryset(self):
        """
        set custom QuerySet to use in manager

        Returns:
            CommentQuerySet: return CommentQuerySet using model Comment
        """
        return CommentQuerySet(self.model, using=self._db)

    def all(self):
        """
        call .all() from CommentQuerySet

        Retruns:
            queryset: return queryset returned from CommentQuerySet.all()
        """
        return self.get_queryset().all()


class Comment(CoreModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField("name", max_length=255, default="unknown")
    comment = models.TextField('comment', help_text='Markdown対応')

    class Meta:
        ordering = ('timestamp', )

    def __str__(self):
        if len(self.comment) > 20:
            return f'{self.comment[:20]}...'
        return self.comment

    def get_comment(self):
        """
        return a cleaned html.
        in case there is a markdown we use markdown package to convert them to html.

        Returns:
            str: string of safe html
        """
        content = self.comment
        markdown_content = markdown(content)
        return mark_safe(markdown_content)
