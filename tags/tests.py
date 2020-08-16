from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Tag


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='example')

    def test_model_created_object(self):
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 1)
        self.assertEqual(self.tag.name, 'example')

    def test_add_active_tag(self):
        second_tag = Tag.objects.create(name='example2')
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 2)
        self.assertEqual(second_tag.name, 'example2')

    def test_add_inactive_tag(self):
        second_tag = Tag.objects.create(name='example2', is_active=False)
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 1)
        self.assertEqual(second_tag.name, 'example2')
