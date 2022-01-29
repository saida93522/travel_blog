from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages


from .models import Author,Post

# Create your views here.
def home(request):
    latest = Post.objects.all()
    context = {"latest":latest}
    return render(request,'blog/home.html',context)

def blog(request):
    context = {}
    return render(request,'blog/blog.html',context)

def post(request):
    context = {}
    return render(request,'blog/post-detail.html',context)

def about(request):
    context = {}
    return render(request,'blog/about.html',context)