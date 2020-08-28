from django import forms

from .models import Article
from tags.models import Tag


class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(
    ), widget=forms.CheckboxSelectMultiple, required=False)
    related_articles = forms.ModelMultipleChoiceField(
        queryset=Article.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    publish_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = Article
        fields = (
            'tags',
            'video',
            'cover',
            'title',
            'description',
            'content',
            'related_articles',
            'keywords',
            'publish_at',
        )
