import os
from PIL import Image

from django.test import TestCase , Client
from django.urls import reverse
from django.http import response
from django.contrib.auth.models import User

from .. import models
from newsletter.models import Subscribers, NewsLetter

class BlogDataTestCase(TestCase):
    """predefine data for blog content."""
    
    def setUp(self):
        
        self.user = User.objects.create_superuser(
            username='bob', 
            email='bob@bobby.com',
            password='admin'
            )

        self.author1 = models.Author.objects.create(
            author=self.user,
            twitter='https://twitter.com',
            instagram='https://instagram.com',
            tiktok='https://tiktok.com',
            philo='my travel philosophy..')
        
         
        self.post1 = models.Post.objects.create(
            owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=False,
            )
        self.country1 = models.Country.objects.create(name='Japan')
        self.post1.country.set([self.country1.pk])        
        
        self.post2 = models.Post.objects.create(
            owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=False,
            )
        self.country2 = models.Country.objects.create(name='Austria')
        self.post2.country.set([self.country2.pk])
        
        self.post3 = models.Post.objects.create(owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,)
        self.country3 = models.Country.objects.create(name='Spain')
        self.post3.country.set([self.country3.pk])
        
        self.post1.save()
        self.post2.save()
        self.post3.save()

class TestHomeViews(BlogDataTestCase):
    def setUp(self):
        # inherit blogdata class data content
        super().setUp()        

    def test_hero_quote_shown_home_page(self):
        " test hopepage hero section shows quotes "
        url = reverse('home')
        
        # object client
        response = self.client.get(url)
        self.assertContains(response, '”A journey of a thousand miles starts with a single step.” – LaoTz')

        #assert included templates 
        self.assertTemplateUsed(response, 'main.html')
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTemplateUsed(response, 'blog/feature_blog.html')
        self.assertTemplateUsed(response, 'blog/subscribe.html')

        #assert unused template false
        self.assertTemplateNotUsed(response, 'blog/blog.html')
        self.assertTemplateNotUsed(response, 'blog/sidebar.html')

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTemplateNotUsed(response, 'blog/blog.html')

    def test_post_is_displayed(self):
        url = reverse('home')
        post = models.Post.objects.all()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(post.count(), 3)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, self.post1.title)
        
    def test_three_latest_post_is_displayed(self):
        url = reverse('home')
        response = self.client.get(url)

        # create another post to validate only first three post are displayed
        post4 = models.Post.objects.create(owner=self.author1,
            title="3 things to do in Japan",
            short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
            created_at='2022-02-18T15:37:32.245078Z',
            is_featured=True,)
        self.country4 = models.Country.objects.create(name='Turkey')
        post4.country.set([self.country4.pk])
        
        expected_qs = models.Post.objects.prefetch_related('country').order_by('-created_at')[0:3]
        self.assertEqual(response.status_code,200)
        self.assertEqual(models.Post.objects.count(),4)
        self.assertEqual(response.context['latest'].count(), expected_qs.count())

        self.assertContains(response, self.post3.title)
        self.assertContains(response, post4.title)

    def test_with_no_post(self):
        url = reverse('home')
        post = models.Post.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response,'No articles published yet!')

    def test_user_can_subscribe(self):
        url = reverse('home')
        data = {
            'email':'mandy123@mandy.com'
            }
        post_response = self.client.post((url),data,follow=True)
        self.assertEqual(post_response.status_code,200)
        self.assertNotEqual(post_response.status_code,404)
        self.assertEqual(Subscribers.objects.count(),1)
        self.assertRedirects(post_response,'/')
        self.assertContains(post_response, 'email')

class TestBlogViews(BlogDataTestCase):
    def setUp(self):
        # call parent class 'setUp' for data content
        super().setUp()

    def test_resolves_correct_page(self):
        url = reverse('blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'BLOG')
        self.assertContains(response, 'Featured Post')

        self.assertTemplateUsed(response, 'blog/blog.html')
        self.assertTemplateUsed(response, 'blog/sidebar.html')
        self.assertTemplateUsed(response, 'blog/banner.html')

    def test_all_blog_page_displays_posts(self):
        url = reverse('blog')
        response = self.client.get(url)
        posts = models.Post.objects.prefetch_related('country').order_by('-created_at')
       
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code,404)

        self.assertEqual(posts.count(),3)
        self.assertTemplateUsed('blog/blog.html')
        self.assertContains(response, self.post1.title)

    def test_featured_blog_post_displayed(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code,200)
        
        self.assertEqual(response.context['featured'].count(),1 )
        self.assertTrue(response.context['featured'])
        self.assertContains(response,'Featured Post')
        self.assertNotEqual(response.context['featured'],False)
        self.assertNotEqual(response.context['featured'], self.post2.is_featured)

        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_blog_post_pagination(self):
        response = self.client.get(reverse('blog'))
        self.assertIn('query_page', response.context)
        self.assertIn('articles', response.context)
        self.assertEqual(response.context['query_page'].count('page'), 1)
        # create 10 blog post + 3 inherited from parent
        for i in range(10):
            models.Post.objects.create(
                owner=self.author1,
                title="3 things to do in Japan",
                short_intro=' Japan! The land of sushi, the Tori and the sumo wrestling!',
                created_at='2022-02-18T15:37:32.245078Z',
                is_featured=False,)

        #access first query page 
        response_page1 = self.client.get(reverse("blog"), {'query_page':1})
        self.assertEqual(response_page1.status_code, 200)
        self.assertEqual(len(list(response_page1.context['articles'])), 4)

        # access out of range page
        response_page2 = self.client.get(reverse("blog"), {'query_page':203})
        self.assertEqual(response_page2.status_code, 200)
        # Check if page out of range, returns last page result
        self.assertEqual(response_page2.context['articles'].number, 1)
        
class TestPostDetail(BlogDataTestCase):
    def setUp(self):
        super().setUp()

    def test_post_exist(self):
        response = self.client.get(reverse('post', kwargs={'pk':self.post1.id}))
        data_rendered = response.context['articles']
        # check returns ok status code
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        # check correct template was used
        self.assertTemplateUsed(response, 'blog/post-detail.html')
        # check same data sent to template
        self.assertEqual(data_rendered, self.post1)
        self.assertEqual(data_rendered.title,'3 things to do in Japan')
        self.assertEqual(data_rendered.short_intro,self.post1.short_intro)
        self.assertEqual(data_rendered.created_at,self.post1.created_at)

        #check correct data shown on page
        self.assertContains(response,'Japan')
        self.assertContains(response,'3 things to do in Japan')
        self.assertIn(self.post1.title, data_rendered.title)

    def test_comments(self):
        data = {
            'name':'sam',
            'email':'samtest@sam',
            'content':'Austria is beautiful.',
            }
        url = reverse('post',kwargs={'pk':self.post2.pk})
       
        post_response = self.client.post((url),data,follow=True)

        data_rendered = post_response.context['form']
        self.assertEqual(post_response.status_code,200)
        
        response = self.client.get(reverse('post',kwargs={'pk':self.post3.pk}))
        self.assertNotEqual(post_response.context['form'],response.context['form'])

        self.assertContains(post_response, 'sam')
        self.assertContains(post_response, 'email')
        self.assertContains(post_response, data['name'])
        self.assertContains(post_response, 'Austria is beautiful.')

        self.assertTemplateUsed(post_response, 'blog/post-detail.html')
        
    def test_create_post_valid(self):
        self.client.login(username='bob',password='admin')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code,302)
        self.assertNotEqual(response.status_code,404)
        self.assertTemplateUsed(response, 'blog/create_post.html')

        # check current blog post
        self.assertEqual(models.Post.objects.count(),3)

        # create new blog post
        new_post = {'title':'test text',
                    'short_intro':'short intro text',
                    'body':'content',
                    
                    }
        new_post['owner'] = self.author1.id
        new_post['country'] = self.country3.id
        post_response = self.client.post(reverse('create_post'),data=new_post,follow=True)
        self.assertEqual(post_response.status_code,200)
        self.assertTemplateUsed(post_response, 'blog/post-detail.html')
        
        # check current blog post
        self.assertEqual(models.Post.objects.count(),4)
        
    def test_create_post_invalid(self):
        self.client.login(username='bob',password='admin')
        data = {'title':'test post title'}
        post_response = self.client.post(reverse('create_post'),data=data,follow=True)
        self.assertEqual(post_response.status_code,200)
        self.assertFormError(post_response,"form","short_intro","This field is required.")

    def test_create_post_link_displayed_for_admin_only(self):
       
        response = self.client.get(reverse('home'))
        self.assertNotContains(response,'Create')
        self.assertTemplateNotUsed(response,'blog/create_post.html')
  

        self.client.login(username='bob',password='admin')
        home_response = self.client.get(reverse('home'))
        create_response = self.client.get(reverse('create_post'))
        
        self.assertContains(home_response,'Create')
        self.assertTemplateUsed(home_response,'blog/home.html')
        self.assertTemplateUsed(create_response,'blog/create_post.html')

    def test_update_post(self):
        self.client.login(username='bob',password='admin')
        data = {
            'short_intro':'test update post'
            }
        response = self.client.post(reverse('update_post',kwargs={'pk':self.post2.pk}),data=data,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'test update post')
        self.assertTemplateUsed(response,'blog/update_post.html')
        
        