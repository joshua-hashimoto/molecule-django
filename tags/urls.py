from django.urls import path

from .views import TagAjaxCreateView

app_name = 'tags'

urlpatterns = [
    path('create/ajax/', TagAjaxCreateView.as_view(), name='tag_ajax_new'),
]
