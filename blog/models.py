from django.db import models
from django.contrib.auth.models import User
from tinymce import HTMLField

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='images')
    twitter = models.CharField(max_length=200,blank=True,null=True)
    instagram = models.CharField(max_length=200,blank=True,null=True)
    tiktok = models.CharField(max_length=200,blank=True,null=True)
    philo = models.TextField(default='')
    bio = HTMLField()
    objects = models.Manager()
    def __str__(self):
        return self.author.username

class Country(models.Model):
    name = models.CharField(max_length=200)
    objects = models.Manager()
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=300)
    body = HTMLField()
    thumbnail =models.ImageField(null=True,blank=True, upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ManyToManyField(Country)    
    is_featured = models.BooleanField(default=False)
    objects = models.Manager()
    # STATUS_CHOICES = (
    # ('draft', 'Draft'),
    # ('published', 'Published'),
    # )
    #status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
   
    def __str__(self):
        return self.owner.author.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50) 
    email = models.EmailField()
    content = models.TextField()
    avatar = models.ImageField(default='default.svg', upload_to='images')
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']
        
    def __str__(self):
        return (f'Comment by {self.name}')


    
        