from django import forms

from newsletter.models import Subscribers, NewsLetter

class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'