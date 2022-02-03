from django.contrib import admin

# Register your models here.
from .models import Subscribers, NewsLetter

admin.site.register(Subscribers)
admin.site.register(NewsLetter)