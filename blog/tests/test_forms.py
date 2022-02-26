from django.test import TestCase
from django.urls import reverse

from blog.forms import PostForm, SubscribersForm, NewsLetterForm, CommentForm
from .test_views import BlogDataTestCase
from .. import models

class TestBlogForm(BlogDataTestCase):
    def setUp(self):
        super().setUp()

    def test_comment(self):
        post = models.Post.objects.get(pk=self.post3.pk)
        data = {'name':'tester',
                'email':'test@email',
                'content':'test body',
                'user_img':models.Comment.user_img}
        
        response = self.client.post(reverse('post',kwargs={'pk':post.pk}),data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tester')
        self.assertContains(response, 'test body')

    def test_missing_email_is_invalid(self):
        form_data = {'name':'test'}
        form = CommentForm(form_data)
        self.assertFalse(form.is_valid())

    def test_subscribe_email_is_valid(self):
        form_data = {'email':'testing@test.com'}
        form = SubscribersForm(form_data)
        self.assertTrue(form.is_valid())

    def test_newsletter_title_and_message_is_valid(self):
        form_data = {'title':'Testing Title','message':'test message'}
        form = NewsLetterForm(form_data)
        self.assertTrue(form.is_valid())