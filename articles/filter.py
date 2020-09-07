from django import forms

import django_filters

from .models import Article
from tags.models import Tag


class ArticleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='search_filter',
        widget=forms.TextInput(attrs={'class': 'uk-search-input', 'placeholder': 'Search...'}))
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__name__iexact',
        to_field_name='name',
        queryset=Tag.objects.all(),
        conjoined=True,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Article
        fields = [
            'search',
            'tags',
        ]

    def search_filter(self, queryset, model_name, value):
        return queryset.search(value)
