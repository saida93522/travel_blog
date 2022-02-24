import os
from PIL import Image

from django.test import TestCase , Client
from django.urls import reverse
from django.http import response
from django.contrib.auth.models import User
# from blog.models import Author, Post, Country, Comment

from .. import models
class TestHomeViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='bob', 
            email='bob@bobby.com',
            password='admin'
            )

        self.author1 = models.Author.objects.create(
            author=self.user,
            twitter='https://twitter.com',
            instagram='https://instagram.com',
            tiktok='https://tiktok.com',
            philo='my travel philosophy..')
        
         
        self.post1 = models.Post.objects.create(
            owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,
            )
        self.country1 = models.Country.objects.create(name='Japan')
        self.post1.country.set([self.country1.pk])        
        
        self.post2 = models.Post.objects.create(
            owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,
            )
        self.country2 = models.Country.objects.create(name='Austria')
        self.post2.country.set([self.country2.pk])
        
        self.post3 = models.Post.objects.create(owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,)
        self.country3 = models.Country.objects.create(name='Spain')
        self.post3.country.set([self.country3.pk])
        
        self.post1.save()
        self.post2.save()
        self.post3.save()
        
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

    def test_post_is_displayed(self):
        url = reverse('home')
        post = models.Post.objects.all()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(post.count(), 3)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, self.post1.title)

        
    def test_three_latest_post_is_displayed(self):
        url = reverse('home')
        response = self.client.get(url)

        # create another post to validate only first three post are displayed
        post4 = models.Post.objects.create(owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,)
        self.country4 = models.Country.objects.create(name='Turkey')
        post4.country.set([self.country4.pk])
        
        expected_qs = models.Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
        self.assertEqual(response.status_code,200)
        self.assertEqual(models.Post.objects.count(),4)
        self.assertEqual(response.context['latest'].count(), expected_qs.count())

        self.assertContains(response, self.post3.title)
        self.assertContains(response, post4.title)

        