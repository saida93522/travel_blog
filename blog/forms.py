from django import forms
from django.forms import ModelChoiceField

from newsletter.models import Subscribers, NewsLetter
from .models import Post

class CommentForm(forms.ModelForm):
    class Meta:
        model: Comment
        fields = ['name','email','body','avatar']
    
class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['title']
