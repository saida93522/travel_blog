from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request,'blog/home.html',context)

def blog(request):
    context = {}
    return render(request,'blog/blog.html',context)

def post(request):
    context = {}
    return render(request,'blog/post-detail.html',context)