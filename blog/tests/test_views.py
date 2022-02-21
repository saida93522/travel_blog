from django.test import TestCase
from django.urls import reverse

from blog.models import Author, Post, Country 

class TestHomePage(TestCase):
    def test_hero_quote_shown_home_page(self):
        " test hopepage hero section shows quotes "
        url = reverse('home')

        # object client
        response = self.client.get(url)
        self.assertContains(response, '”A journey of a thousand miles starts with a single step.” – LaoTz')

        #assert included templates 
        self.assertTemplateUsed(response, 'main.html')
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTemplateUsed(response, 'blog/feature_blog.html')
        self.assertTemplateUsed(response, 'blog/subscribe.html')

        #assert unused template false
        self.assertTemplateNotUsed(response, 'blog/sidebar.html')

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    