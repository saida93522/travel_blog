""" Handles all of the specific url routes of the blog app,
queries from db or templates that need to be rendered. """ 



""" links specific URL(urlpath) to the defined views(urlHandler)."""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('blog/',views.blog, name='blog'),
    path('post/',views.post, name='post'),
    path('about/',views.about, name='about'),
    
]


