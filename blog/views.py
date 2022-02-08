from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from newsletter.models import Subscribers, NewsLetter
from .forms import SubscribersForm, NewsLetterForm
from .utils import get_country

from .models import Author, Country, Post

def home(request):
    latest_post = Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
    form = SubscribersForm(request.POST)
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully signed up for our newsletter.')
            return redirect('/')
    else:
        form = SubscribersForm()
    context = {"latest":latest_post, 'form':form}
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
    articles = Post.objects.prefetch_related('country')
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
    blog_post = Post.objects.get(id=pk)
    country_count = get_country()
    context = {'articles':blog_post, 'country_count':country_count}
    return render(request,'blog/post-detail.html',context)

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
        print(latest_post)
    context = {'form':form}
    return render(request, 'newsletter.html',context)






def about(request):
    context = {}
    return render(request,'blog/about.html',context)