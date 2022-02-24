import os
from PIL import Image

from django.test import TestCase , Client
from django.urls import reverse
from django.http import response
from django.contrib.auth.models import User
# from blog.models import Author, Post, Country, Comment

from .. import models
from newsletter.models import Subscribers, NewsLetter

class BlogDataTestCase(TestCase):
    """predefine data for blog content."""
    
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
            is_featured=False,
            )
        self.country1 = models.Country.objects.create(name='Japan')
        self.post1.country.set([self.country1.pk])        
        
        self.post2 = models.Post.objects.create(
            owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=False,
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

class TestHomeViews(BlogDataTestCase):
    def setUp(self):
        # inherit blogdata class data content
        super().setUp()        
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

    def test_with_no_post(self):
        url = reverse('home')
        post = models.Post.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response,'No articles published yet!')

    def test_user_can_subscribe(self):
        url = reverse('home')
        data = {
            'email':'mandy123@mandy.com'
            }
        post_response = self.client.post((url),data,follow=True)
        self.assertEqual(post_response.status_code,200)
        self.assertNotEqual(post_response.status_code,404)
        self.assertEqual(Subscribers.objects.count(),1)
        self.assertRedirects(post_response,'/')
        self.assertContains(post_response, 'email')


class TestBlogViews(BlogDataTestCase):
    def setUp(self):
        # call parent class 'setUp' for data content
        super().setUp()

    def test_resolves_correct_page(self):
        url = reverse('blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'BLOG')
        self.assertContains(response, 'Featured Post')

        self.assertTemplateUsed(response, 'blog/blog.html')
        self.assertTemplateUsed(response, 'blog/sidebar.html')
        self.assertTemplateUsed(response, 'blog/banner.html')

        

    def test_all_post_displayed(self):
      pass