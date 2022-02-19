from django.db import models
import uuid
from blog.models import Post
from tinymce.models import HTMLField

class Subscribers(models.Model):
    email = models.EmailField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    objects = models.Manager()

    def __str__(self):
        return self.email


class NewsLetter(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    message = HTMLField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    

    def __str__(self):
        return self.title
    