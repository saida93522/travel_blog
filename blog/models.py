from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='images')
    objects = models.Manager()
    def __str__(self):
        return self.author.username
    
class Post(models.Model):
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=300)
    body = models.TextField()
    thumbnail =models.ImageField(null=True,blank=True, upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # STATUS_CHOICES = (
    # ('draft', 'Draft'),
    # ('published', 'Published'),
    # )
    #status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    def __str__(self):
        return self.owner.author.username
    