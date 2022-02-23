import os
from PIL import Image

from django.test import TestCase , Client
from django.urls import reverse
from django.http import response
from django.contrib.auth.models import User
from blog.models import Author, Post, Country, Comment

from .. import models
class TestHomeViews(TestCase):
    fixtures = ['blog/fixtures/testing_users.json','blog/fixtures/testing_author.json','blog/fixtures/testing_posts.json']
    # def setUp(self):
    #     self.user = User.objects.create_superuser(
    #         username='bob', 
    #         email='bob@bobby.com',
    #         password='admin'
    #         )
    #     self.author1 = models.Author(
    #         author=self.user,
    #         twitter='https://twitter.com',
    #         instagram='https://instagram.com',
    #         tiktok='https://tiktok.com',
    #         philo='my travel philosophy..')
        
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
        self.assertTemplateNotUsed(response, 'blog/blog.html')
        self.assertTemplateNotUsed(response, 'blog/sidebar.html')

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTemplateNotUsed(response, 'blog/blog.html')

    def test_three_latest_post_is_displayed(self):
        pass
    def test_three_latest_post_is_displayed(self):
        pass