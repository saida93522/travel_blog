from django.test import TestCase
from django.urls import reverse, resolve

from .. import views

class TestURLS(TestCase):
    def test_home_url_resolves(self):
        """ Test url resolves and returns blog url. """
        
        url = reverse('home')
        response = resolve(url).func
        self.assertEqual(response, views.home)
        self.assertEqual(resolve('/').func, views.home)
    def test_blog_url_resolves(self):
        """ Test url resolves and returns blog url. """
        
        url = reverse('blog')
        response = resolve(url).func
        self.assertEqual(response, views.blog)
        self.assertNotEqual(response, views.home)

    def test_post_url_resolves(self):
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

    def test_create_post_url_resolves(self):
        """ Test url resolves and returns create_post url. """
        
        url = reverse('create_post')
        response = resolve(url).func
        self.assertEqual(response, views.create_post)
        self.assertNotEqual(response, views.update_post)
        
    def test_update_post_url_resolves(self):
        """ Test url resolves and returns update_post url. """
        
        url = reverse('update_post', kwargs={'pk':'ad45g39f'})
        # set url to resolve of post,id
        response = resolve(url).func
        self.assertEqual(response, views.update_post)

        url2 = reverse('update_post', kwargs={'pk':'dc78339d'})
        response2 = resolve(url2).func
 
        self.assertNotEqual(response, views.blog)
        self.assertNotEqual(response, views.create_post)
        self.assertNotEqual([resolve(url).kwargs,resolve(url2).kwargs], views.update_post)

    def test_delete_post_urls_resolves(self):
        """ Test url resolves and returns delete_post url. """
        
        url = reverse('delete_post', kwargs={'pk':'a756kgk'})
        response = resolve(url).func
        self.assertEqual(response, views.delete_post)
        self.assertNotEqual(response, views.update_post)

    def test_about_url_resolves(self):
        """ Test url resolves and returns about url. """
        
        url = reverse('about')
        response = resolve(url).func
        self.assertEqual(response, views.about)
        self.assertNotEqual(response, views.home)
        self.assertNotEqual(response, views.blog)

    def test_newsletter_url_resolves(self):
        """ Test url resolves and returns newsletter url. """
        
        url = reverse('news_letter')
        response = resolve(url).func
        self.assertEqual(response,views.news_letter)
        self.assertNotEqual(response,views.search)
        self.assertNotEqual(response,views.home)
        self.assertNotEqual(response,views.blog)

    def test_search_url_resolves(self):
        """ Test url resolves and returns search url. """
        
        url = reverse('search')
        response = resolve(url).func
        self.assertEqual(response,views.search)
        self.assertNotEqual(response,views.blog)
        self.assertNotEqual(response,views.post)
