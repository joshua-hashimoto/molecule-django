import os
import json
import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import cloudinary

from .models import Article
from .filter import ArticleFilter
from .forms import ArticleForm


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
    paginate_by = 28
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


class ArticleDetailView(DetailView):
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Passes form class for creating new object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        form_class (ArticleForm): set custom Forms
        template_name (str): a path to template that is responsible to render objects
        success_url (str): a named url to go to after creation is successful
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_new.html'
    success_url = reverse_lazy('articles:article_list')
    login_url = 'admin'

    def form_valid(self, form):
        """
        Default function for CreateView that is called when
        the form user submits is valid.
        Override to set current login user to user field in model.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """
    Passes form class for creating new object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        form_class (ArticleForm): set custom Forms
        template_name (str): a path to template that is responsible to render objects
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_edit.html'
    login_url = 'admin'

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
        return reverse_lazy('articles:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an existing object.
    Login is required.

    Attributes:
        model (Article): target model to fetch data from.
        template_name (str): a path to template that is responsible to render objects.
                             for the moment this is a dummy sense delete does not have a template
        success_url (str): a named url to go to after creation is successful
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Article
    template_name = 'articles/article_detail.html'
    success_url = reverse_lazy('articles:article_list')
    login_url = 'admin'

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


class MarkdownImageUploader(View):
    """
    custom image uploader for martor.
    """

    def post(self, request, *args, **kwargs):
        """
        called when images are uploaded to martor's markdown field.
        validation is from martor's documentation.
        it will upload images to cloudinary.

        Note:
            when there is '?' in the to be foldername the image upload will not work.
        """
        article_title = request.POST['title']
        if not article_title:
            return HttpResponse(_('Invalid request!'))

        if not request.is_ajax():
            return HttpResponse(_('Invalid request!'))

        if 'markdown-image-upload' not in request.FILES:
            return HttpResponse(_('Invalid request!'))

        image = request.FILES['markdown-image-upload']
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            # return error when the image type
            # is not an expected type
            data = json.dumps({
                'status': 405,
                'error': _('Bad image format.')
            }, cls=LazyEncoder)
            return HttpResponse(
                data, content_type='application/json', status=405)

        if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
            # return error when the image size
            # is over the setted MAX_IMAGE_UPLOAD_SIZE
            to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
            data = json.dumps({
                'status': 405,
                'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
            }, cls=LazyEncoder)
            return HttpResponse(
                data, content_type='application/json', status=405)

        # when the image is valid

        # create new name for image
        img_name = f'{uuid.uuid4().hex[:10]}-{image.name.replace(" ", "-")}'
        # assign new name to the image that is being uploaded
        image.name = img_name
        # create folder path
        img_folder = os.path.join(
            settings.MEDIA_URL, f'article/{article_title}/markdown/')
        # save image to cloudinary
        cloudinary_img = cloudinary.uploader.upload(
            image, folder=img_folder, overwrite=True)
        # get the saved image url from cloudinary response
        cloudinary_img_url = cloudinary_img['url']
        # name json data to return to markdown
        data = json.dumps({
            'status': 200,
            'link': cloudinary_img_url,
            'name': image.name
        })
        return HttpResponse(data, content_type='application/json')
