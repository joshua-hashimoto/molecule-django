from django import forms

from .models import Comment


class CommentCreateForm(forms.ModelForm):
    verify = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'uk-input', 'placeholder': '「分子」をひらがなで入力してください'}))

    class Meta:
        model = Comment
        fields = ('verify', 'name', 'comment',)
