from django import forms
from tinymce.widgets import TinyMCE

from newsletter.models import Subscribers, NewsLetter
from .models import Post,Comment,Author


class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self, *args):
		return False


class PostForm(forms.ModelForm):
	body = forms.CharField(
		widget=TinyMCEWidget(
			attrs={'required': False,'cols': 70, 'rows': 30}
		)
	)
	class Meta:
		model = Post
		fields = ['title','short_intro','body', 'thumbnail','country','is_featured']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','content','avatar']
    
class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']

class NewsLetterForm(forms.ModelForm):
    message = forms.CharField(widget=TinyMCEWidget(attrs={'required':False, 'cols':70, 'rows':30}))
    class Meta:
        model = NewsLetter
        fields = ['title','message']
