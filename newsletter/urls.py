from django.urls import path
from . import views

urlpatterns = [
    path('newsletter/', views.news_letter, name='news_letter'),
]
