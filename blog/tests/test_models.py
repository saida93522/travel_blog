from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
# from blog.models import Author, Post, Country
from .. import models

class TestAuthor(TestCase):
    def test_author_creation(self):
        """Test one to one relationship
        """
        user = User.objects.create_superuser(
            username='bob', 
            email='bob@bobby.com',
            password='admin')
        user.save()
        #Create author 
        author1 = models.Author(author=user,philo='my travel philosophy..')
        author1.save()
        #assert Author is instance of user
        self.assertIsInstance(user.author, models.Author)
        