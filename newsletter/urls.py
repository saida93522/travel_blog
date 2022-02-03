from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_up, name=sign_up),
    path('newsletter/', views.news_letter, name=news_letter),
]
