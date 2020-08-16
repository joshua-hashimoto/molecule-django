from django.urls import path

from .views import CommentCreateView

app_name = 'comments'

urlpatterns = [
    path('new/', CommentCreateView.as_view(), name='comment_new'),
]
