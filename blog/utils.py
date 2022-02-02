from django.db.models import Count
from .models import Post, Country

def get_country():
    queryset = Post.objects.values('country__name').annotate(Count('country__name'))
    return queryset