from datetime import datetime
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .models import MyUser, Profile
from django.urls import reverse
from .forms import LoginForm, RegistrationForm

from datetime import datetime

class MeTestView(TestCase):
    def setUp(self) -> None:
        MyUser.objects.create(email="test@gmail.com",
                              username = 'goldlin',
                              password = make_password("123"),
                              created_at = datetime.now(),
                              updated_at = datetime.now())

    def test_user_attr_type(self):
        us = MyUser.objects.get(email='test@gmail.com')
        self.assertEqual(type(us.email), str)
        self.assertEqual(type(us.username), str)
        self.assertEqual(type(us.password), str)
        self.assertEqual(type(us.created_at), type(datetime.now()))
        self.assertEqual(type(us.updated_at), type(datetime.now()))

    def test_page(self):
        resp = self.client.get(reverse('login'), follow=True)
        resp2 = self.client.get(reverse('registration'), follow=True)
        self.assertTrue(resp.status_code in (200, 302))
        self.assertTrue(resp2.status_code in (200, 302))
        self.assertTemplateUsed(resp, 'me/login.html')
        self.assertTemplateUsed(resp2, 'me/registration.html')

class MeFormTest(TestCase):
    def setUp(self):
        self.form = LoginForm(data={'email':'gg@gmail.com','password' : 'hgfdrtgf', 'remember':True})
        self.form_2 = LoginForm(data={'email':'gg','password' : 'hgfdrtgf', 'remember':True})

    def test_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_invalid(self):
        self.assertFalse(self.form_2.is_valid())
        


        
