from django.contrib import admin
from django.db import models
# from django_summernote.admin import SummernoteModelAdmin
from martor.widgets import AdminMartorWidget
from django.utils import timezone

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    """
    custom admin for model Phrase

    Attributes:
        list_desplay (List): list of fields in model to display in admin site
        list_display_links (List): list of fields in model to attach links to in admin site
        list_filter (List): list of fields in model that the user can filter through in admin site
        search_fields (List): list of fields in model that the user can search through in admin site
        actions (List): list of custom functions to add custom actions to admin site
        inlines (List): list of custom Inline classes to add relational fields in admin site
    """

    list_display = [
        'id',
        'title',
        'truncated_description',
        'is_published',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'title',
        'is_active',
    ]
    search_fields = [
        'title',
        'description',
        'content',
    ]
    actions = ['active', 'inactive']

    def active(self, request, queryset):
        """
        function to set the target model's "is_active" to True.
        used in admin site.
        """
        queryset.update(is_active=True)

    active.short_description = '閲覧可能'

    def inactive(self, request, queryset):
        """
        function to set the target model's "is_active" to False.
        used in admin site.
        """
        queryset.update(is_active=False)

    inactive.short_description = '閲覧不可能'

    def truncated_description(self, obj):
        """
        custom admin column.
        call get_description on model.

        Returns:
            str: truncated string
        """
        return obj.get_description()

    truncated_description.short_description = "description"

    def is_published(self, obj):
        """
        custom admin column.
        if publish_at field has no data, it will return string 'no publish date'.
        if publish_at field has data and current time is over the 
        object data, it will return string 'published'.
        if publish_at field has data and is before current time it will return the field value.

        Args:
            obj (Article): data object.

        Returns:
            datetime|str: publish status.
        """
        if (publish_at := obj.publish_at):
            now = timezone.now()
            if now > publish_at:
                return 'published'
            return publish_at
        return 'no publish date'

    is_published.short_description = 'publish status'


admin.site.register(Article, ArticleAdmin)