from django.test import TestCase

from apps.accounts.forms import UserModelForm
from apps.blogapp.forms import *

from apps.blogapp.models import *


class TestForms(TestCase):

    def setUp(self) -> None:
        category = Category.objects.create(name='test_category', depth='1')
        user = get_user_model().objects.create(email='test_user@bk.ru', password='1')
        user2 = get_user_model().objects.create(email='test_user2@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, author=user, descr='test_descr',
                                         content='test_content', slug='test_article')

    def test_article_form(self):
        category = Category.objects.get(pk=1)
        form = ArticleModelForm(data={
            'name': 'test_name',
            'descr': 'descr',
            'category': category.pk,
            'content': 'content',
            'slug': 'slug',
            'comments_count': 123,
            'likes_count': 123,
        }
        )
        self.assertTrue(form.is_valid())

    def test_user_form(self):
        form = UserModelForm(initial={'email': 'asdasdasd@bk.ru'},data={
            'email': 'asdasdasd@bk.ru',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '+380663868458',

        }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())
