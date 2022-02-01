from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Author, Country, Post

# Create your views here.
def home(request):
    lates_post = Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
    context = {"latest":lates_post}
    return render(request,'blog/home.html',context)

def blog(request):
    articles = Post.objects.prefetch_related('country')
    # articles = Post.objects.all()
    featured = Post.objects.filter(is_featured=True)

    
    context = {'featured':featured,'articles':paginated_page,'page_req':page_req}
    return render(request,'blog/blog.html',context)

def post(request,pk):
    blog_post = Post.objects.get(id=pk)
    context = {'blog_post':blog_post}
    return render(request,'blog/post-detail.html',context)

def about(request):
    context = {}
    return render(request,'blog/about.html',context)