from http import HTTPStatus as status_code

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Article
from tags.models import Tag


"""
Note:
    because image and video uploads are handled by 
    the cloudinary library we will not test it here
"""


class ArticleModelTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser1234',)
        self.tag = Tag.objects.create(
            name='example tag',)
        self.article = Article.objects.create(
            author=self.user,
            title='example',
            description='example description',
            content='#example',
            keywords='example',
            publish_at='2020-01-01 00:00',)
        self.second_article = Article.objects.create(
            author=self.user,
            title='example2',
            description='example description',
            content='#example2',
            keywords='example2',
            publish_at='2020-01-01 00:00',)
        self.second_article.tags.set([self.tag.id])
        self.second_article.related_articles.set([self.article.id])

    def test_model_created_articles(self):
        queryset = Article.objects.all()
        self.assertEqual(queryset.count(), 2)

    def test_inactive_object(self):
        article = Article.objects.create(
            author=self.user,
            title='example3',
            description='example description',
            content='#example3',
            keywords='example3',
            publish_at='2020-01-01 00:00',
            is_active=False,)
        queryset = Article.objects.all()
        self.assertEqual(queryset.count(), 2)

    def test_model_can_search(self):
        queryset = Article.objects.search('2')
        self.assertEqual(queryset.count(), 1)
        queryset = Article.objects.search('asdgdg')
        self.assertEqual(queryset.count(), 0)


class ArticleViewTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser1234',)
        self.tag = Tag.objects.create(
            name='example tag',)
        self.article = Article.objects.create(
            author=self.user,
            title='example',
            description='example description',
            content='#example',
            keywords='example',
            publish_at='2020-01-01 00:00',)
        self.second_article = Article.objects.create(
            author=self.user,
            title='example2',
            description='example description',
            content='#example2',
            keywords='example2',
            publish_at='2020-01-01 00:00',)
        self.second_article.tags.set([self.tag.id])
        self.second_article.related_articles.set([self.article.id])
        self.third_article = Article.objects.create(
            author=self.user,
            title='example3',
            description='example description',
            content='#example3',
            keywords='example3',)

    def test_article_list_view_for_logged_in_user(self):
        self.client.login(username='testuser', password='testuser1234')
        response = self.client.get(reverse('articles:article_list'))
        self.assertEqual(response.status_code, status_code.OK)
        self.assertContains(response, 'example')
        self.assertContains(response, 'example2')
        # logged in user can see the unpublished article
        self.assertContains(response, 'example3')
        # check if tag is rendered to template
        self.assertContains(response, 'example tag')
        self.assertTemplateUsed(response, 'articles/article_home.html')
        self.assertTemplateUsed(response, 'articles/article_accordion.html')
        self.assertTemplateUsed(
            response, 'articles/article_detail_content.html')
        self.assertTemplateUsed(response, 'widgets/pagination.html')

    def test_article_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('articles:article_list'))
        self.assertEqual(response.status_code, status_code.OK)
        self.assertContains(response, 'example')
        self.assertContains(response, 'example2')
        # check if tag is rendered to template
        self.assertContains(response, 'example tag')
        self.assertTemplateUsed(response, 'articles/article_home.html')
        self.assertTemplateUsed(response, 'articles/article_accordion.html')
        self.assertTemplateUsed(
            response, 'articles/article_detail_content.html')

    def test_article_detail_view(self):
        self.client.logout()
        response = self.client.get(
            reverse('articles:article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, status_code.OK)
        self.assertContains(response, 'example')
        self.assertTemplateUsed(response, 'articles/article_detail.html')
        self.assertTemplateUsed(
            response, 'articles/article_detail_content.html')
        no_response = self.client.get('/molecule/1234/')
        self.assertEqual(no_response.status_code, 404)

    def test_display_article_create_view(self):
        self.client.login(username='testuser', password='testuser1234')
        response = self.client.get(reverse('articles:article_new'))
        self.assertEqual(response.status_code, status_code.OK)
        self.assertTemplateUsed(response, 'articles/article_base_form.html')
        self.assertTemplateUsed(response, 'articles/article_new.html')

    def test_logged_out_user_cannot_access_article_create_view(self):
        self.client.logout()
        response = self.client.get(reverse('articles:article_new'))
        self.assertEqual(response.status_code, status_code.NOT_FOUND)

    def test_post_article_create_view(self):
        self.client.login(username='testuser', password='testuser1234')
        data = {
            'title': 'example4',
            'description': 'example description',
            'content': '#example4',
            'keywords': 'example4',
            'publish_at': '2020-01-01 00:00'
        }
        response = self.client.post(reverse('articles:article_new'), data=data)
        self.assertEqual(response.status_code, status_code.FOUND)
        self.assertRedirects(response, reverse('articles:article_list'))

    def test_post_fails_article_create_view(self):
        self.client.login(username='testuser', password='testuser1234')
        data = {
            'title': 'example2',
            'description': 'example description',
            'content': '#example4',
            'keywords': 'example4',
            'publish_at': '2020-01-01 00:00'
        }
        response = self.client.post(reverse('articles:article_new'), data=data)
        self.assertEqual(response.status_code, status_code.OK)
        self.assertFormError(response, 'form', 'title',
                             'この Title を持った Article が既に存在します。')

    def test_display_article_update_view(self):
        self.client.login(username='testuser', password='testuser1234')
        response = self.client.get(
            reverse('articles:article_edit', kwargs={'pk': self.second_article.pk}))
        self.assertEqual(response.status_code, status_code.OK)
        self.assertTemplateUsed(response, 'articles/article_base_form.html')
        self.assertTemplateUsed(response, 'articles/article_edit.html')

    def test_logged_out_user_cannot_access_article_update_view(self):
        self.client.logout()
        response = self.client.get(
            reverse('articles:article_edit', kwargs={'pk': self.second_article.pk}))
        self.assertEqual(response.status_code, status_code.NOT_FOUND)

    def test_post_article_update_view(self):
        self.client.login(username='testuser', password='testuser1234')
        data = {
            'title': 'example2 edit',
            'description': 'example description',
            'content': '#example2',
            'keywords': 'example2',
            'publish_at': '2020-01-01 00:00'
        }
        response = self.client.post(reverse('articles:article_edit', kwargs={
                                    'pk': self.second_article.pk}), data=data)
        self.assertEqual(response.status_code, status_code.FOUND)
        self.assertRedirects(response, reverse(
            'articles:article_detail', kwargs={'pk': self.second_article.pk}))
        response = self.client.get(reverse(
            'articles:article_detail', kwargs={'pk': self.second_article.pk}))
        self.assertContains(response, 'example2 edit')

    def test_post_fails_article_update_view(self):
        self.client.login(username='testuser', password='testuser1234')
        data = {
            'title': 'example',
            'description': 'example description',
            'content': '#example2',
            'keywords': 'example2',
            'publish_at': '2020-01-01 00:00'
        }
        response = self.client.post(reverse('articles:article_edit', kwargs={
                                    'pk': self.second_article.pk}), data=data)
        self.assertEqual(response.status_code, status_code.OK)
        self.assertFormError(response, 'form', 'title',
                             'この Title を持った Article が既に存在します。')
