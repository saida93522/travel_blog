from django.db.models import Count
from .models import Post, Country, Author
from .forms import SubscribersForm
def get_country():
    queryset = Post.objects.values('country__name').annotate(Count('country__name'))
    return queryset




# def subscribe():
#     form = SubscribersForm(request.POST or None, request.FILES or None)
#     if request.method == 'POST':
#         form = SubscribersForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'You have successfully signed up for our newsletter.')
#             return redirect('/')
#     else:
#         form = SubscribersForm()
#     return form