from django.test import TestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .. import models
from .. import views

class TestURLS(TestCase):
    def test_home_urls_is_resolves(self):
        """ Test url resolves and returns blog url. """
        
        url = reverse('home')
        response = resolve(url).func
        self.assertEqual(response, views.home)


    def test_blog_urls_is_resolves(self):
        """ Test url resolves and returns blog url. """

        url = reverse('blog')
        response = resolve(url).func
        self.assertEqual(response, views.blog)
        self.assertNotEqual(response, views.home)

    def test_post_urls_is_resolves(self):
        """ Test url resolves and returns post url. """

        # set url to resolve of post,id
        url = reverse('post', kwargs={'pk':'ad45g39f'})
        response = resolve(url).func
        self.assertEqual(response, views.post)

        url2 = reverse('post', kwargs={'pk':'dc78339d'})
        response2 = resolve(url2).func
 
        self.assertNotEqual(response, views.home)
        self.assertNotEqual(response, views.blog)
        self.assertNotEqual([resolve(url).kwargs,resolve(url2).kwargs], views.post)


    def test_create_post_urls_is_resolves(self):
        """ Test url resolves and returns create_page url. """
        
        url = reverse('create_post')
        response = resolve(url).func
        self.assertEqual(response, views.create_post)
        self.assertNotEqual(response, views.update_post)