from django.test import TestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .. import models
from .. import views

class TestURLS(TestCase):
    def test_home_urls_is_resolved(self):
        # set url to resolve of home
        url = reverse('home')
        response = resolve(url).func
        self.assertEqual(response, views.home)


    def test_blog_urls_is_resolved(self):
        # set url to resolve of home
        url = reverse('blog')
        response = resolve(url).func
        self.assertEqual(response, views.blog)
        self.assertNotEqual(response, views.home)


    def test_create_post_urls_is_resolved(self):
        # set url to resolve of home
        url = reverse('create_post')
        response = resolve(url).func
        self.assertEqual(response, views.create_post)
        self.assertNotEqual(response, views.update_post)