from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404

from .models import Comment
from .forms import CommentCreateForm
from articles.models import Article


class CommentCreateView(View):
    """
    a view to create comments
    """

    def post(self, request):
        """
        a django default method called on a post request to the view.
        when the comment is created email will be send to the blog creator.
        the flow is the flowing,
        1. check if the article_slug exists in the data.
           if not, send a error message and redirect to home page
        2. check if the form is valid.
           if not send a error message and redirect to detail page with the article_slug
        3. check if the value of 'verify' is correct.
           if not send a error message and redirect to detail page with the article_slug
        4. get the article object using the article_slug
        5. execute form.save(commit=False)
        6. attach article to comment
        7. execute form.save()
        8. send email to creator of the blog(not post)
        9. redirect to detail page with the article_slug
        """
        article_slug = request.POST.get('article_slug')
        if not article_slug:
            messages.error(request, '問題が発生しました。もう一度お試しください :(')
            return redirect('articles:article_list')

        form = CommentCreateForm(request.POST or None)
        if form.is_valid():
            verified_word = form.cleaned_data.get('verify')
            if verified_word != 'ぶんし':
                messages.error(request, '認証が通りませんでした。もう一度お試しください :(')
                return redirect('articles:article_detail', slug=article_slug)
            target_article = get_object_or_404(Article, slug=article_slug)
            comment = form.save(commit=False)
            comment.article = target_article
            comment.save()
            self.send_email_notification(
                comment=comment, article=target_article)
            messages.success(request, "コメントを残しました :)")
        else:
            messages.error(request, "コメントを残すことができませんでした :(")
        return redirect('articles:article_detail', slug=article_slug)

    def send_email_notification(self, comment, article):
        """
        method to send email.
        for message content we load the template txt file.
        """
        subject = 'You have a new comment'
        context_data = {
            'article': article,
            'comment': comment,
        }
        message = render_to_string(
            'mails/comment_notification_email.txt', context_data, self.request)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, recipient_list)
