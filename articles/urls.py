from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'articles'

urlpatterns = [
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<uuid:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<uuid:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<uuid:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('', ArticleListView.as_view(), name='article_list'),
]
