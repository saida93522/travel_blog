from django.contrib import admin
from .models import Post, Author , Country, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Country)
admin.site.register(Comment)