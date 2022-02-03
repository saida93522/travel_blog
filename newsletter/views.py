from django.shortcuts import render
from .forms import SubscribersForm, NewsLetterForm
# Create your views here.
def sign_up(request):
    """ validates subscribers email
    """
    form = SubscribersForm()

    context = {}
    return render(request, 'blog/subscribe.html',context)


def news_letter(request):
    context = {}
    return render(request, 'blog/newsletter.html',context)
    
