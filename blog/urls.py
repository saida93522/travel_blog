""" Handles all of the specific url routes of the blog app,
queries from db or templates that need to be rendered. """ 



""" links specific URL(urlpath) to the defined views(urlHandler)."""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('blog/',views.blog, name='blog'),
    path('post/<str:pk>/',views.post, name='post'),

    #CRUD
    path('create_post/',views.create_post, name='create_post'),
    path('post/<str:pk>/update/',views.update_post, name='update_post'),
    path('post/<str:pk>/delete/',views.delete_post, name='delete_post'),


    # Profile
    path('about/',views.about, name='about'),

    # newsletter
    path('newsletter/', views.news_letter, name='news_letter'),
    path('search/', views.search, name='search'),
    
]


