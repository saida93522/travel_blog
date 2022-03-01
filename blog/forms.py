from django import forms
from django.forms import ValidationError
from django.contrib import messages
from django.core.validators import validate_email
from tinymce.widgets import TinyMCE

from newsletter.models import Subscribers, NewsLetter
from .models import Post, Comment, Author

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
        fields = ['name','email','content','user_img']
    
class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        error_msg = {'email_exists':'This email already exists'}
        # if not email:
        #     raise ValidationError(error_msg['invalid_email'], code='invalid')
        if Subscribers.objects.filter(email__iexact=email).exists():
            raise ValidationError(error_msg['email_exists'], code='exists')
        else:
            try:
                validate_email(email)
                return email
            except ValidationError as ve:
                return ve
        return email

    def save(self,commit=True):
        user = super(SubscribersForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        # validators.validate_email(user.email)
        if commit:
            user.save()
        return user

class NewsLetterForm(forms.ModelForm):
    message = forms.CharField(widget=TinyMCEWidget(attrs={'required':False, 'cols':70, 'rows':30}))
    class Meta:
        model = NewsLetter
        fields = ['title','message']