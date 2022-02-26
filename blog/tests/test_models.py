from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
# from blog.models import Author, Post, Country
from .. import models
from .test_views import BlogDataTestCase


class TestBlogModel(BlogDataTestCase):
    def setUp(self):
        super().setUp()
      
    def test_instance_creation(self):
        """Test one to one relationship
        """
        #assert objects instance of models
        self.assertIsInstance(self.user.author, models.Author)
        self.assertIsInstance(self.country1, models.Country)
        self.assertIsInstance(self.post2, models.Post)
        

    def test_str_representation(self):
        """Test author model returns string representation"""
        self.assertEqual(self.author1.__str__(), self.author1.author.username)
        self.assertEqual(self.post1.__str__(), self.post1.owner.author.username)
        self.assertEqual(self.country1.__str__(), self.country1.name)

    def test_auto_field_datetime(self):
        post = models.Post.objects.get(pk=self.post2.pk)
        self.assertIsNotNone(post.created_at)
        old_time = post.created_at
        post.title = 'Test time updates'
        post.save()
        self.assertTrue(post.created_at == old_time)



