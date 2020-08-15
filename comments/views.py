from django.contrib import messages
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404

from .models import Comment
from .forms import CommentCreateForm
from articles.models import Article


class CommentCreateView(View):
    """
    """

    def post(self, request):
        article_id = request.POST.get('article_id')
        if not article_id:
            messages.error(request, '問題が発生しました。もう一度お試しください :(')
            return redirect('articles:article_list')

        form = CommentCreateForm(request.POST or None)
        if form.is_valid():
            verified_word = form.cleaned_data.get('verify')
            if verified_word != 'ぶんし':
                messages.error(request, '認証が通りませんでした。もう一度お試しください :(')
                return redirect('articles:article_detail', pk=article_id)
            target_article = get_object_or_404(Article, pk=article_id)
            comment = form.save(commit=False)
            comment.article = target_article
            comment.save()
            messages.success(request, "コメントを残しました :)")
        else:
            messages.error(request, "コメントを残すことができませんでした :(")
        return redirect('articles:article_detail', pk=article_id)
