from django.contrib import admin

from .models import Tag


def active(self, request, queryset):
    queryset.update(is_active=True)


active.short_description = '閲覧可能'


def inactive(self, request, queryset):
    queryset.update(is_active=False)


inactive.short_description = '閲覧不可能'


class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    actions = [active, inactive]


admin.site.register(Tag, TagAdmin)
