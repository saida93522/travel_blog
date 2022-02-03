from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import NewsLetterForm
# Create your views here.



def news_letter(request):
    context = {}
    return render(request, 'blog/newsletter.html',context)
    
