from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone

from cloudinary_storage.storage import VideoMediaCloudinaryStorage, MediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
from markdown import markdown
from martor.models import MartorField
from bs4 import BeautifulSoup

from core.additional.models import CoreModel
from tags.models import Tag


class ArticleQuerySet(models.QuerySet):
    """
    custom QuerySet for model Article
    """

    def all(self):
        """
        Returns:
            queryset: return all object with is_active=True
        """
        queryset = self.filter(is_active=True)
        return queryset

    def published(self):
        """
        return all objects that is,
        1. is_active is True
        2. publish_at is over the current datetime

        Returns:
            queryset: return all objects that meats the lookup
        """
        now = timezone.now()
        lookup: Q = (
            Q(is_active=True) &
            Q(publish_at__lte=now)
        )
        queryset = self.filter(lookup)
        return queryset

    def search(self, query: str):
        """
        filter objects that is,
        1. is_active is True
        2. publish_at is  over the current datetime
        3. query is contained in title
        4. query is contained in content
        5. query is contained in description

        Returns:
            queryset: return all objects that meats the lookup
        """
        now = timezone.now()
        lookup: Q = (
            Q(is_active=True) &
            Q(publish_at__lte=now) &
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        queryset = self.filter(lookup)
        return queryset


class ArticleManager(models.Manager):
    """
    custom manager for model Article using ArticleQuerySet
    """

    def get_queryset(self):
        """
        set custom QuerySet to use in manager

        Returns:
            ArticleQuerySet: return ArticleQuerySet using model Article
        """
        return ArticleQuerySet(self.model, using=self._db)

    def all(self):
        """
        call .all() from ArticleQuerySet

        Retruns:
            queryset: return queryset returned from ArticleQuerySet.all()
        """
        queryset = self.get_queryset().all()
        return queryset

    def published(self):
        """
        call .published() from ArticleQuerySet

        Returns:
            queryset: return queryset returned from ArticleQuerySet.published()
        """
        queryset = self.get_queryset().published()
        return queryset

    def search(self, query=None):
        """
        call .search() from ArticleQuerySet
        if argument query is not set it will return None

        Args:
            query (str|None): user input query

        Returns:
            queryset|None: return queryset returned from ArticleQuerySet.search()
        """
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


def upload_image_to(instance, filename):
    """
    custom path for saving images

    Returns:
        str: image path
    """
    asset_path = f'article/{str(instance.title)}/images/{filename}'
    return asset_path


def upload_video_to(instance, filename):
    """
    custom path for saving videos

    Returns:
        str: video path
    """
    asset_path = f'article/{str(instance.title)}/video/{filename}'
    return asset_path


class Article(CoreModel):
    """
    A model for representing each article for the blog.

    Attributes:
        author (ForeignKey): one-to-one relation to set user to object
        tags (ManyToManyField): many-to-many relation to set tags to object
        video (FileField): field for video files. saved to cloudinary
        cover (ImageField): field for image files. saved to cloudinary
        title (CharField): field for article title. max length to 255. this field needs to be unique
        description (TextField): field for article description.
        content (MartorField): field for article content. uses martor's MartorField for markdown.
        related_article (ManyToManyField): many-to-many relation to set self as related articles
        keywords (CharField): field for article keyword. this is used for SEO.
        publish_at (DateTimeField) field for article publish datetime.
        objects (ArticleManager): set custom Manager to model

    Note:
        because ImageField and DateTimeField saves string in 
        the database, null=True is not necessary.
    """
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    video = models.FileField(upload_to=upload_video_to, blank=True, null=True,
                             storage=VideoMediaCloudinaryStorage(), validators=[validate_video])
    cover = models.ImageField(
        upload_to=upload_image_to, blank=True, null=True, storage=MediaCloudinaryStorage())
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    content = MartorField()
    related_articles = models.ManyToManyField(
        'self', verbose_name='related articles', blank=True)
    keywords = models.CharField('記事のキーワード', max_length=255, default='プログラミング')
    publish_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)

    objects = ArticleManager()

    class Meta:
        """
        Attributes:
            ordering (List): use to determine the ordering of model objects when listed
        """
        ordering = ['-publish_at', '-timestamp', '-updated', ]

    def __str__(self):
        """
        determine which field of the model should be representing the model object.
        mainly used in admin site.

        Returns:
            str: returns title field.
        """
        return self.title

    def get_absolute_url(self):
        """
        determine to absolute url of the model.
        mainly used to route to detail view.
        """
        return reverse("articles:article_detail", kwargs={"pk": self.pk})

    def get_markdown(self):
        """
        return a cleaned html.
        in case there is a markdown we use markdown to convert them to html.

        Returns:
            str: string of safe html
        """
        content = self.content
        markdown_content = markdown(content)
        return mark_safe(markdown_content)

    def get_description(self):
        """
        return description. if the description str length
        is greater then 50 it truncates the str.

        Returns:
            str: truncated string
        """
        if len(self.description) > 50:
            return f"{self.description[:50]}..."
        return self.description

    def get_text_count(self):
        """
        count strings in html.
        using BeautifulSoup4 to sanitize html tags.

        Returns:
            int: length of the string after sanitized by BeautifulSoup4
        """
        content = self.content
        markdown_content = markdown(content)
        souped = BeautifulSoup(markdown_content, features="html.parser").findAll(
            text=True
        )
        stripted_text = "".join(souped).replace(" ", "")
        return len(stripted_text)

    def get_img_count(self):
        """
        count img tags in html.
        using BeautifulSoup4 search through html.

        Returns:
            int: length of the images after filtering through using BeautifulSoup4
        """
        content = self.content
        markdown_content = markdown(content)
        img_tags = BeautifulSoup(markdown_content, features="html.parser").find_all(
            "img"
        )
        return len(img_tags)
