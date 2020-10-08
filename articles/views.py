from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Article
from .filter import ArticleFilter
from .forms import ArticleForm
from .permissions import AccessPermissionToUsers, PublishPermission
from comments.forms import CommentCreateForm


class ArticleListView(ListView):
    """
    List all objects in model to template.

    Attributes:
        template_name (str): a path to template that is responsible to render objects
        context_object_name (str): to override context object name used in template.
                                   for ListView's it defaults to 'object_list'
        paginate_by (int): int to set pagination. for example if you set 10
                           object_list will be separated by 10 and the resulting
                           number will be the pagination length.
    """
    template_name = 'articles/article_home.html'
    context_object_name = 'article_list'
    paginate_by = 20
    form_class = ArticleFilter

    def get_queryset(self):
        """
        Overriding this method will give the developer more
        controll over objects that will be passed to the template.
        In regular cases this is not needed using django-filter.
        However in this case we needed to change the object_list
        depending on whether the user is logged in or not. In the
        case of this application author is the only user who can
        be logged in. If the visitor is logged in to the application
        we want all objects including the unpublished objects to show up too.

        1. get all published objects
        2. if user is authenticated, get all objects that is is_active=True
        3. use ArticleFilter to filter through the objects

        Returns:
            queryset: return filtered queryset

        Notes:
            if there is a way to override queryset within django-filter
            to only implement the if-user-of-not function, switch
            to that because overriding get_queryset can result
            in security issues.
        """
        queryset = Article.objects.published()
        if self.request.user.is_authenticated:
            queryset = Article.objects.all()
            # queryset = (queryset | user_queryset).distinct()
        queryset = ArticleFilter(
            self.request.GET, queryset=queryset)
        return queryset.qs

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add data to pass to template.
        """
        context = super().get_context_data(**kwargs)
        context["filter"] = self.form_class(self.request.GET or None)
        return context


class ArticleDetailView(PublishPermission, DetailView):
    """
    Passes a single object to template.

    Attributes:
        model (Article): target model to fetch data from
        template_name (str): a path to template that is responsible to render objects
        context_object_name (str): to override context object name used in template
                                   for DetailView's it defaults to 'object'
    """
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm(self.request.POST or None)
        return context


class ArticleCreateView(AccessPermissionToUsers, CreateView):
    """
    Passes form class for creating new object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        form_class (ArticleForm): set custom Forms
        template_name (str): a path to template that is responsible to render objects
        success_url (str): a named url to go to after creation is successful
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:article_list')

    def form_valid(self, form):
        """
        Default function for CreateView that is called when
        the form user submits is valid.
        Override to set current login user to user field in model.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(AccessPermissionToUsers, UpdateView):
    """
    Passes form class for creating new object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        form_class (ArticleForm): set custom Forms
        template_name (str): a path to template that is responsible to render objects
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'

    def form_valid(self, form):
        """
        Default function for CreateView that is called when
        the form user submits is valid.
        Override to set current login user to user field in model.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Default function for UpdateView that is called when
        the update is successful.
        Override to give a url to go to after the update is success.
        """
        return reverse_lazy('articles:article_detail', kwargs={'slug': self.object.slug})


class ArticleDeleteView(AccessPermissionToUsers, DeleteView):
    """
    Delete an existing object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        template_name (str): a path to template that is responsible to render objects.
                             for the moment this is a dummy sense delete does not have a template
        success_url (str): a named url to go to after creation is successful
    """
    model = Article
    template_name = 'articles/article_detail.html'
    success_url = reverse_lazy('articles:article_list')

    def delete(self, request, *args, **kwargs):
        """
        Override this method to change the delete behavior.
        In this case instead of deleting we set the is_active
        field to False so it will not appear to the user.
        A full deletion must happen in the admin site.

        Returns:
            HttpResponseRedirect: redirects the page to a givin url
        """
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
