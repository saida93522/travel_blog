from django import forms
from django.forms import ModelChoiceField

from newsletter.models import Subscribers, NewsLetter
from .models import Post
class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']


# class ModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, field):
#         return f"{field}"


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['title']
         
         
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user','')
    #     super(NewsLetterForm, self).__init__(*args, **kwargs)
    #     self.fields =forms.ModelChoiceField(queryset=Post.objects.filter(owner=user))
        #   self.fields['unique_code']=forms.CharField(max_length=15)