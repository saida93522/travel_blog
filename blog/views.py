from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
# from django.contrib.auth import login

from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from newsletter.models import Subscribers, NewsLetter
from .forms import PostForm, SubscribersForm, NewsLetterForm, CommentForm
from .utils import get_country

from .models import Author, Country, Post, Comment

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
    
    country_count = get_country()
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
    
    context = {'featured':featured,
               'articles':paginated_page,
             
               'query_page':query_page,
               'country_count':country_count}
    return render(request,'blog/blog.html',context)

def post(request,pk):
    country_count = get_country()
    blog_post = get_object_or_404(Post, id=pk)
    
    comments = blog_post.comments.filter(is_active=True)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # create comment
            new_comment = form.save(commit=False)
            # Assign post to comment
            new_comment.post = blog_post
            new_comment.save()
    else:
        form = CommentForm()
    context = {'articles':blog_post,
             
               'country_count':country_count, 
               'form':form, 
               'new_comment':new_comment,
               'comments':comments}
    return render(request,'blog/post-detail.html',context)

def get_user(author):
    qs = Author.objects.filter(author=author)
    if qs.exists():
        return qs[0]
    return None

def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    owner = get_user(request.user)
   
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = owner
            form.save()
            return redirect('post', pk=form.instance.id)
    context = {'form':form}
    return render(request,'blog/create_post.html',context)

def update_post(request,pk):
    post = get_object_or_404(Post, id=pk)
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


def news_letter(request):
    emails = Subscribers.objects.all()
    mail_list = [mail for mail in emails]
    print(mail_list)
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            send_mail(
                title,
                'message',
                'tinywanderlust@example.com', 
                mail_list,
                fail_silently=False,
                )
            
            messages.success(request, 'Your email has been sent to subscribers successfully.')
            return redirect('news_letter')
    else:
        form = NewsLetterForm()
 
    context = {'form':form}
    return render(request, 'newsletter.html',context)

def about(request):
    context = {}
    return render(request,'blog/about.html',context)