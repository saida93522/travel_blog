from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import NewsLetterForm
from .models import Subscribers, NewsLetter
# Create your views here.



# def news_letter(request):
#     if request.method == 'POST':
#         form = NewsLetterForm(request.POST)
#         form.save()
#         message.success(request, 'Your email has been sent to subscribers successfully.')
#         return redirect('/')
#     else:
#         form = NewsLetterForm()
#     context = {'form':form}
#     return render(request, 'newsletter.html',context)
    
