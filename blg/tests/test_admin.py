from django.contrib.auth import get_user_model

from apps.accounts.admin import *
from django.test import TestCase

from apps.accounts.models import User


class TestAdmin(TestCase):

    def test_main_create_user(self):
        user = get_user_model().objects.create_user('jdoe@gmail.com', 'password123')
        self.assertTrue(isinstance(user, get_user_model()))

    def test_main_create_superuser(self):
        user = get_user_model().objects.create_superuser('jdoe@gmail.com', 'password123')
        self.assertTrue(isinstance(user, get_user_model()))

    def test_main_create_user_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='password123')

    def test_main_create_superuser_is_staff(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser('jdoe@gmail.com', 'password123', is_staff=False)

    def test_main_create_superuser_is_superuser(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser('jdoe@gmail.com', 'password123', is_superuser=False)
