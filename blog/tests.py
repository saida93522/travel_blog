from django.test import TestCase
from django.urls import reverse

from .models import Author, Post, Country 

class TestHomePage(TestCase):
    def test_hero_quote_shown_home_page(self):
        " test hopepage hero section shows quotes "
        url = reverse('home')

        # object client
        response = self.client.get(url)
        self.assertContains(response, '”A journey of a thousand miles starts with a single step.” – LaoTz')