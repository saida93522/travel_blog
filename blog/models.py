from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    # feature_image =models.ImageField(null=True, blank=True)
    # STATUS_CHOICES = (
    # ('draft', 'Draft'),
    # ('published', 'Published'),
    # )
    #status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

