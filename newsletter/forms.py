from django import forms

from .models import Subscribers, Newsletter

class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'