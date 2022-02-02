from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import get_country
from .models import Author, Country, Post

# Create your views here.
def home(request):
    lates_post = Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
    context = {"latest":lates_post}
    return render(request,'blog/home.html',context)

def blog(request):
    articles = Post.objects.prefetch_related('country')
    featured = Post.objects.filter(is_featured=True)
    #render queryset in pages 4
    paginator = Paginator(articles,4)

    # parameter used to determine what instances or page in the queryset needs to be rendered
    query_page = 'page'
    page_req = request.GET.get(query_page)

    try:
        paginated_page = paginator.page(page_req)
    except PageNotAnInteger:
        paginated_page = paginator.page(1)
    except EmptyPage:
        #display last page result if page is out of range
        paginated_page = paginator.page(paginator.num_pages)
    

    
    context = {'featured':featured, 'articles':paginated_page, 'query_page':query_page}
    return render(request,'blog/blog.html',context)

def post(request,pk):
    blog_post = Post.objects.get(id=pk)
    country_count = get_country()
    context = {'articles':blog_post, 'country_count':country_count}
    return render(request,'blog/post-detail.html',context)

def about(request):
    context = {}
    return render(request,'blog/about.html',context)