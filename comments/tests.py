from http import HTTPStatus as status

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Comment
from articles.models import Article


class CommentModelTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser1234',)
        self.article = Article.objects.create(
            author=user,
            title='example',
            slug='example',
            description='example description',
            content='#example',
            keywords='example',
            publish_at='2020-01-01 00:00',)
        self.comment = Comment.objects.create(
            article=self.article,
            name='unknown',
            comment='comment example',)

    def test_model_created_comment(self):
        queryset = Comment.objects.all()
        self.assertEqual(queryset.count(), 1)

    def test_model_create_inactive_comment(self):
        queryset = Comment.objects.all()
        Comment.objects.create(
            article=self.article,
            name='unknown',
            comment='comment example 2',
            is_active=False,)
        self.assertEqual(queryset.count(), 1)

    def test_comment_related_to_article(self):
        Comment.objects.create(
            article=self.article,
            name='unknown',
            comment='comment example 2',)
        comments = self.article.comments.all()
        self.assertEqual(comments.count(), 2)


class CommentViewTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser1234',)
        self.article = Article.objects.create(
            author=user,
            title='example',
            slug='example',
            description='example description',
            content='#example',
            keywords='example',
            publish_at='2020-01-01 00:00',)
        self.comment = Comment.objects.create(
            article=self.article,
            name='unknown',
            comment='comment example',)

    def test_comment_create_view_can_create_comment(self):
        context_data = {
            'verify': 'ぶんし',
            'article_slug': self.article.slug,
            'name': 'unknown',
            'comment': '# comment',
        }
        response = self.client.post(
            reverse('comments:comment_new'), data=context_data)
        self.assertEqual(response.status_code, status.FOUND)
        self.assertRedirects(response, reverse(
            'articles:article_detail', kwargs={'slug': self.article.slug}))
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 2)

    def test_comment_fail_with_verification(self):
        context_data = {
            'verify': '分子',
            'article_slug': self.article.slug,
            'name': 'unknown',
            'comment': '# comment',
        }
        response = self.client.post(
            reverse('comments:comment_new'), data=context_data)
        self.assertEqual(response.status_code, status.FOUND)
        self.assertRedirects(response, reverse(
            'articles:article_detail', kwargs={'slug': self.article.slug}))
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

    def test_comment_fail_with_no_article_id(self):
        context_data = {
            'verify': 'ぶんし',
            'name': 'unknown',
            'comment': '# comment',
        }
        response = self.client.post(
            reverse('comments:comment_new'), data=context_data)
        self.assertEqual(response.status_code, status.FOUND)
        self.assertRedirects(response, reverse(
            'articles:article_list'))
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

    def test_comment_fail_with_form_error(self):
        context_data = {
            'verify': '分子',
            'article_slug': self.article.slug,
            'name': '',
            'comment': '# comment',
        }
        response = self.client.post(
            reverse('comments:comment_new'), data=context_data)
        self.assertEqual(response.status_code, status.FOUND)
        self.assertRedirects(response, reverse(
            'articles:article_detail', kwargs={'slug': self.article.slug}))
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)
