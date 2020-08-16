from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
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
        'truncated_comment',
        'article',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'article',
        'is_active',
    ]
    search_fields = [
        'comment',
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

    def truncated_comment(self, obj):
        """
        custom admin column.

        Returns:
            str: truncated string
        """
        if len(obj.comment) > 20:
            return f'{obj.comment[:20]}...'
        return obj.comment

    truncated_comment.short_description = "comment"


admin.site.register(Comment, CommentAdmin)
