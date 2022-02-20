from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.exceptions import *

from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from newsletter.models import Subscribers, NewsLetter
from .forms import PostForm, SubscribersForm, NewsLetterForm, CommentForm
from .utils import get_country, subscribe,get_pagination

from .models import Author, Country, Post, Comment
import re



def home(request):
    intro = Author.objects.all()
    posts = Post.objects.prefetch_related('country')
    latest_post = posts.order_by('-created_at')[0:3]
    form = SubscribersForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully signed up for our newsletter.')
            return redirect('/')
    else:
        form = SubscribersForm()
    context = {"latest":latest_post,'intro':intro, 'form':form}
    return render(request,'blog/home.html',context)

def search(request):
    articles = Post.objects.prefetch_related('country')
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query)|
            Q(short_intro__icontains=query)|
            Q(country__name__icontains=query)
            ).distinct()
 
    context = {'articles':articles,'q':query}
    return render(request,'blog/search.html',context)

def blog(request):
    articles = Post.objects.prefetch_related('country').order_by('-created_at')
    paginated_page,query_page =  get_pagination(request,articles)

    country_count = get_country()
    featured = Post.objects.filter(is_featured=True)
    
    form = subscribe(request)
    
        
    context = {'featured':featured,
               'articles':paginated_page,
               'query_page':query_page,
               'form':form,
               'country_count':country_count}
    return render(request,'blog/blog.html',context)

def post(request,pk):
    country_count = get_country()
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.filter(is_active=True)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            # create comment
            new_comment = form.save(commit=False)
            # Assign post to comment
            new_comment.post = post
            new_comment.save()
            messages.success(request,('Added comment successfully'))
            return redirect('post',pk=post.id)
    else:
        form = CommentForm()
    context = {'articles':post,
             
               'country_count':country_count, 
               'form':form, 
               'new_comment':new_comment,
               'comments':comments}
    return render(request,'blog/post-detail.html',context)


# CRUD
def create_post(request):
    owner = request.user.author
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = owner
            messages.success(request,('Post was added successfully!'))
            new_post.save()
            return redirect('post', pk=new_post.id)
    context = {'form':form}
    return render(request,'blog/create_post.html',context)

def update_post(request,pk):
    owner = request.user.author
    post = owner.post_set.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Post was successfully updated.')
            return redirect('post',pk=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form':form, 'post':post}
    return render(request,'blog/update_post.html',context)

def delete_post(request,pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    messages.error(request,('Post was deleted successfully!'))
    return redirect('blog')

def clean_msg(msg):
    CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    clean = re.sub(CLEANER,'',msg)
    return clean

def news_letter(request):
    emails = Subscribers.objects.all()
    mail_list = [mail for mail in emails]
    print(mail_list)
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            email_msg = clean_msg(message)
            
            send_mail(
                title,
                email_msg,
                'tinywanderlust@example.com', 
                mail_list,
                fail_silently=False,
                )
            
            messages.success(request, 'Your email has been sent to subscribers successfully.')
            return redirect('news_letter')
    else:
        form = NewsLetterForm()
 
    context = {'form':form}
    return render(request, 'blog/newsletter.html',context)

def about(request):
    author = Author.objects.all()
    country_count = get_country()
    context={'country_count':country_count, 'author':author}
    return render(request,'blog/about.html',context)