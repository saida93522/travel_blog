from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages


from .models import Author,Country,Post

# Create your views here.
def home(request):
    lates_post = Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
    context = {"latest":lates_post}
    return render(request,'blog/home.html',context)

def blog(request):
    articles = Post.objects.prefetch_related('country').order_by('-created_at')
    # related_post = Post.objects.order_by('-created_at')
    context = {'articles':articles}
    return render(request,'blog/blog.html',context)

def post(request):
    context = {}
    return render(request,'blog/post-detail.html',context)

def about(request):
    context = {}
    return render(request,'blog/about.html',context)