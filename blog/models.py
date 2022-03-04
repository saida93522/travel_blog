from django.db import models
from django.contrib.auth.models import User
import uuid
from tinymce.models import HTMLField
from django.core.files.storage import default_storage

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='images')
    twitter = models.CharField(max_length=200,blank=True,null=True)
    instagram = models.CharField(max_length=200,blank=True,null=True)
    tiktok = models.CharField(max_length=200,blank=True,null=True)
    philo = models.TextField(default='')
    bio = HTMLField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    objects = models.Manager()
    
    def __str__(self):
        return self.author.username

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)   
    objects = models.Manager()
    def __str__(self):
        return self.name
    
class Post(models.Model):
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    short_intro = models.CharField(max_length=300)
    body = HTMLField()
    thumbnail =models.ImageField(upload_to='images',default='yashc.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ManyToManyField(Country,blank=True)    
    is_featured = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        #get reference to previous  thumbnail img
        old_thumbnail = Post.objects.filter(pk=self.pk).first()
        if old_thumbnail and old_thumbnail.thumbnail:
            if old_thumbnail.thumbnail != self.thumbnail:
                self.delete_thumbnail(old_thumbnail.thumbnail)
                
        super().save(*args, **kwargs)

    def delete_thumbnail(self, thumbnail):
        if default_storage.exists(thumbnail.name):
            default_storage.delete(thumbnail.name)
            
   
    def __str__(self):
        return self.owner.author.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50) 
    email = models.EmailField()
    content = models.TextField()
    user_img = models.ImageField(upload_to='images', default='default.jpg')
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return (f'Comment by {self.name}')


    
        