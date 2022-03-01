from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Post, Country, Author
from .forms import SubscribersForm

def get_country():
    queryset = Post.objects.values('country__name').annotate(Count('country__name'))
    return queryset


def get_pagination(request,articles):
    # country_count = get_country()
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

    return paginated_page , query_page

def subscribe(request):
    form = SubscribersForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            new_sub = form.save(commit=False)
            messages.success(request, 'You have successfully signed up for our newsletter.')
            new_sub.save()
            return redirect(reverse('blog') + "#subscribe")
        else:
            messages.error(request,form.errors['email'])
            return (reverse('blog') + "#subscribe")
    else:
        form = SubscribersForm(request.POST)
    return form

def subscribe2(form):
    # generate form with email data from request
    
    if form.is_valid():
        sub_email = form.save(commit=False)
        sub_email.save()
        messages.success(request, 'You have successfully signed up for our newsletter.')
        return redirect('blog')
    else:
        # redirect to subscribe section and display error message
        messages.error(request,form.errors['email'])
    
