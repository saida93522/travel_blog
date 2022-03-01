from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import Subscribers, NewsLetter
# Create your views here.

def handle_not_found(request, exception):
    return render (request,'404.html')

