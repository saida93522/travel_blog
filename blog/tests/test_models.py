from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
# from blog.models import Author, Post, Country
from .. import models

class TestAuthor(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='bob', 
            email='bob@bobby.com',
            password='admin')
        self.author1 = models.Author(
            author=self.user,
            philo='my travel philosophy..')
        
    def test_author_creation(self):
        """Test one to one relationship
        """
        #assert Author is instance of user
        self.assertIsInstance(self.user.author, models.Author)

    def test_str_representation(self):
         """Test author model returns string representation"""
        self.assertEqual(self.author1.__str__(), self.author1.author.username)



class TestPostModel(TestCase):
    pass