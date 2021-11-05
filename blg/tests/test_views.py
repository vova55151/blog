from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

import apps.blogapp.views as bv
import apps.accounts.views as av
from apps.blogapp.models import Article, Category, Comment


# TODO: coverage report --omit=parser/parser.py,apps/blogapp/task.py -m

class TestRestViews(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='test_category', depth='1')
        user = get_user_model().objects.create(email='test_user@bk.ru', password='1')
        user2 = get_user_model().objects.create(email='test_user2@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, author=user, descr='test_descr',
                                         content='test_content', slug='test_article')

    def test_call_view_deny_anonymous_update_rest(self):
        response = self.client.post('/ru/rest/api/v1/test_article/update/', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_call_view_deny_anonymous_create_rest(self):
        category = Category.objects.get(pk=1)
        response = self.client.post('/ru/rest/api/v1/create/',
                                    {
                                        'name': 'test_name',
                                        'descr': 'descr',
                                        'category': str(category.pk),
                                        'content': 'content',
                                        'slug': 'slug',
                                        'comments_count': '123',
                                        'likes_count': '123',

                                    }, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_call_view_create_rest(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        category = Category.objects.get(pk=1)
        self.client.post('/ru/rest/api/v1/create/',
                         {
                             'name': 'test_name',
                             'descr': 'descr',
                             'category': str(category.pk),
                             'content': 'content',
                             'slug': 'slug',
                             'comments_count': '123',
                             'likes_count': '123',

                         }, follow=True)
        self.assertEqual(Article.objects.get(slug='slug').name, 'test_name')

    def test_call_view_FavouritesAddView(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get('/ru/rest/api/v1/test_article/fav/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_FavouritesAddView_remove(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        self.client.get('/ru/rest/api/v1/test_article/fav/', follow=True)
        response = self.client.get('/ru/rest/api/v1/test_article/fav/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_unsub(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        self.client.get(f'/ru/{article.slug}/detail/', follow=True)
        self.client.get(f'/ru/rest/api/v1/1/sub', follow=True)
        response = self.client.get(f'/ru/rest/api/v1/1/sub', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_user_update(self):
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(f'/ru/rest/api/v1/profile/update/', {  # TODO: данные передаются гетом,а не постом
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': 'phone',

        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_call_view_user_detail(self):
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(f'/ru/rest/api/v1/profile/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_user_update(self):
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(f'/ru/rest/api/v1/profile/update/', {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': 'phone',

        }, follow=True)
        self.assertEqual(response.status_code, 200)


class TestBlogappViewsPost(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='test_category', depth='1')
        user = get_user_model().objects.create_superuser(email='test_user@bk.ru', password='1')
        user2 = get_user_model().objects.create(email='test_user2@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, author=user, descr='test_descr',
                                         content='test_content', slug='test_article')
        # article = Article.objects.create(slug='asdgaer', article_short_overview='ewarear',
        #                                  article_content='srthrtghjnrtjh',
        #                                  author=Author.objects.create_superuser(email='user12@gmail.com',
        #                                                                         password='123'),
        #                                  category=Category.objects.create(category_name='lolipop1',
        #                                                                   category_slug='lolipop1',
        #                                                                   depth=1, path=546),
        #                                  article_name='qweteqrtqer',
        #                                  )
        #
        # self.comment_ = Comment.objects.create(article=article, comment_name='Alex',
        #                                        comment_content='aehaerthaethaeh')
        #
        # self.comment = {
        #     'article': article.slug,
        #     'comment_name': 'Alex',
        #     'comment_content': 'aehaerthaethaeh',
        #     'comment_rating': 1
        # }
        # self.client.force_login(Author.objects.get(email='user12@gmail.com'))
        # self.response = self.client.post('/uk/blog/asdgaer/add/', self.comment, follow=True)
        #
        # self.com = CommentCreateView()

    def test_meta_model(self):
        model = bv.Filter.Meta.model
        self.assertEquals(model, Article)


class TestBlogappViews(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='test_category', depth='1',
                                           slug='test_category',
                                           path=546)
        user = get_user_model().objects.create_superuser(email='test_user@bk.ru', password='1')
        user2 = get_user_model().objects.create(email='test_user2@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, author=user, descr='test_descr',
                                         content='test_content', slug='test_article')
        # self.context_update = {
        #     'name': 'Test_name',
        #     'descr': 'test_descr',
        #     'content': 'test_content',
        #     'slug': 'test_article',
        #     'comments_count': '0',
        #     'likes_count': '0',
        #     'category': str(category.pk),
        #     'author': str(get_user_model().objects.get(pk=1)),
        #     'rating': str(0),
        #     'my_order': '0',
        #
        # }
        self.context_create = {
            'name': 'Test_name',
            'descr': 'test_descr',
            'category': str(category.pk),
            'content': 'test_content',
            'slug': 'test_slug',
            'comments_count': '0',
            'likes_count': '0',

        }

        # art = Article.objects.get(slug='test_slug').refresh_from_db()
        # print(art)

    def test_meta_model(self):
        model = bv.Filter.Meta.model
        self.assertEquals(model, Article)

    def test_call_view_deny_anonymous_blog(self):
        response = self.client.post('/ru/create/', follow=True)
        self.assertRedirects(response, '/ru/accounts/login/?next=%2Fru%2Fcreate%2F')

    def test_get_absolute_url(self):
        article = Article.objects.get(pk=1)
        self.assertEquals(article.get_absolute_url(), f'/ru/{str(article.slug)}/detail/')

    def test_call_view_deny_anonymous_update_article(self):
        article = Article.objects.get(pk=1)
        response = self.client.post(f'/ru/{article.slug}/update/', follow=True)
        self.assertRedirects(response, '/ru/accounts/login/?next=%2Fru%2Ftest_article%2Fupdate%2F')

    def test_succesfull_redirect_update_article(self):
        category = Category.objects.get(pk=1)
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

        response = self.client.post(
            f'/ru/test_article/update/',
            self.context_create
        )
        self.assertEqual(response.status_code,
                         200)

    def test_create_article_post_invalid(self):
        category = Category.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

        response = self.client.post(
            f'/ru/create/',
        )

        self.assertEqual(response.status_code, 200)

    def test_create_article_post_valid(self):
        category = Category.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

        response = self.client.post(
            f'/ru/create/',
            self.context_create,

        )
        # print(Article.objects.get(slug='test_slug'))
        # from pprint import pprint
        # pprint(response.__dict__)
        # print(Article.objects.get(slug='slug'))
        # # TODO : форма валидна ,form_valid не покрыт тестами
        self.assertEqual(response.status_code, 200)

    def test_create_article_get(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(
            f'/ru/create/',
            follow=True
        )

        self.assertEqual(response.status_code, 200)

    def test_call_view_template_used_article_update(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        category = Category.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(
            reverse('blogapp:update', kwargs={'slug': article.slug}),
            {'name': 'Test_name', 'descr': 'test_descr', 'content': 'test_content', 'category': category}, follow=True)
        self.assertTemplateUsed(response, 'blogapp/article_update.html')

    def test_article_list_view(self):
        response = self.client.get(
            f'/ru/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_create(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

        response = self.client.post(  # TODO: rest comment create
            f'/ru/test_article/comment/',
            {
                'author': user,
                'article': article.slug,
                'text': 'test_text',
                'status': 'P',
                'rating': '1',

            },
            follow=True

        )
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view_403(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.post(f'/ru/{article.slug}/delete/', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_article_detail_view_200(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(f'/ru/{article.slug}/delete/', follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_get_object_CommentCreateView(self):
    #     comment = bv.CommentCreateView()
    #     self.assertIsNotNone(comment.get_object())


class TestAccountsViews(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='test_category', depth='1')
        user = get_user_model().objects.create(email='test_user@bk.ru', password='1')
        user2 = get_user_model().objects.create(email='test_user2@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, author=user, descr='test_descr',
                                         content='test_content', slug='test_article')

    def test_call_view_deny_anonymous(self):
        article = Article.objects.get(pk=1)
        response = self.client.get(f'/profile/fav/{article.slug}/', follow=True)
        self.assertRedirects(response, '/ru/accounts/login/?next=%2Fru%2Fprofile%2Ffav%2Ftest_article%2F')
        response = self.client.post(f'/profile/fav/{article.slug}/', follow=True)
        self.assertRedirects(response, '/ru/accounts/login/?next=%2Fru%2Fprofile%2Ffav%2Ftest_article%2F')

    def test_call_view_load_fav(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(f'/profile/fav/{article.slug}/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_load_unfav(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(f'/profile/fav/{article.slug}/', follow=True)
        response = self.client.get(f'/profile/fav/{article.slug}/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_load_sublist(self):
        self.client.login(email='test_user@bk.ru', password='1')
        response = self.client.get(f'/profile/sublist/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_logout_redirect(self):
        self.client.login(email='test_user@bk.ru', password='1')
        response = self.client.get(f'/profile/logout/', follow=True)
        self.assertRedirects(response, reverse('blogapp:home'))

    def test_call_view_sublist(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get('/profile/sublist/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_favlist(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get('/profile/fav/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_sub(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        self.client.get(f'/ru/{article.slug}/detail/', follow=True)
        response = self.client.get(f'/ru/profile/{article.author.pk}/sub?next=/ru/{article.slug}/detail/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_unsub(self):
        article = Article.objects.get(pk=1)
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)

        self.client.get(f'/ru/{article.slug}/detail/', follow=True)
        self.client.get(f'/ru/profile/{article.author.pk}/sub', follow=True)
        response = self.client.get(f'/ru/profile/{article.author.pk}/sub', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_get(self):
        user = get_user_model().objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(f'/ru/profile/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_post(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(
            f'/ru/profile/edit/',
            {
                'email': 'Test_name',
                'first_name': 'test_descr',
                'last_name': 'test_content',
                'phone': 'test_article',
            },
            follow=True

        )

        self.assertEqual(response.status_code, 200)

    def test_user_profile_post_form_invalid(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(
            f'/ru/profile/edit/',
            {
                'email': '',
                'first_name': 'test_descr',

                'phone': '',
            },
            follow=True

        )

        self.assertEqual(response.status_code, 200)

    def test_user_profile_password(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(
            f'/ru/profile/pass_update/',
            {
                'old_password': '1',
                'new_password1': 'test_password123',
                'new_password2': 'test_password123',
            },
            follow=True

        )

        self.assertEqual(response.status_code, 200)
