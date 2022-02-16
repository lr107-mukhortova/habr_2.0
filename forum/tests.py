from django.test import TestCase
from .models import Post, Tag
from .forms import PostForm
from me.models import MyUser
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from datetime import datetime

class ForumTestView(TestCase):
    def setUp(self) -> None:
        MyUser.objects.create(email="test@gmail.com",
                              username = 'goldlin',
                              password = make_password("123"),
                              created_at = datetime.now(),
                              updated_at = datetime.now())
                              
        Post.objects.create(model_name = 'ggg',
                            short_description = 'ttt',
                            full_description = 'feve',
                            ref_on_git = 'https://github.com',
                            created_at = datetime.now(),
                            updated_at = datetime.now(),
                            user = MyUser.objects.get(email='test@gmail.com'))

        

        

    def test_form_attr(self):
        post = Post.objects.get(model_name='ggg')
        self.assertEqual(type(post.model_name), str)
        self.assertEqual(type(post.short_description), str)
        self.assertEqual(type(post.full_description), str)
        self.assertEqual(type(post.ref_on_git), str)
        self.assertEqual(type(post.created_at), type(datetime.now()))
        self.assertEqual(type(post.updated_at), type(datetime.now()))

    def test_templates(self):
        resp = self.client.get(reverse('posts'), follow=True)
        resp2 = self.client.get(reverse('main_page'), follow=True)
        self.assertTrue(resp.status_code in (200, 302))
        self.assertTrue(resp2.status_code in (200, 302))
        self.assertTemplateUsed(resp, 'forum/all_posts.html')
        self.assertTemplateUsed(resp2, 'forum/main_page.html')

class PostFormTest(TestCase):
    def setUp(self):
        self.form = PostForm(data={'mdoel_name':'ggg',
                                    'short_description':'efer',
                                    'full_description':'csdcds',
                                    'ref_on_git':'https://github'})
        
        self.form_2 = PostForm(data={'mdoel_name':'ggg',
                                    'short_description':'efer',
                                    'full_description':'csdcds',
                                    'ref_on_git':'h'})

    def test_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_invalid(self):
        self.assertFalse(self.form_2.is_valid())