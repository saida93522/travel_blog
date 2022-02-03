from django.db import models

# Create your models here.

class Subscribers(models.Model):
    email = models.EmailField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.email


class NewsLetter(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.title
    