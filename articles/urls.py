from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'articles'

urlpatterns = [
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('', ArticleListView.as_view(), name='article_list'),
]
