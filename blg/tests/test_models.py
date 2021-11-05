from django.test import TestCase

from apps.blogapp.models import *


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='test_category', depth='1')
        Category.objects.create(name='test_category1', depth='2', path='path1')
        Category.objects.create(name='test_category2', depth='3', path='path2')

    def test_name_label(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_autocreate_slug(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('slug')
        self.assertIsNotNone(field_label)

    def test_name_max_length(self):
        category = Category.objects.get(pk=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_get_absolute_url(self):
        category = Category.objects.get(pk=1)
        self.assertEquals(category.get_absolute_url(), '/?author=&category=1&name=&o=')

    def test__str__(self):
        category = Category.objects.get(pk=1)
        self.assertEquals(category.__str__(), f'{category.name}')

    def test__str__2(self):
        category = Category.objects.get(pk=2)
        self.assertEquals(category.__str__(), f'-{category.name}')

    def test__str__3(self):
        category = Category.objects.get(pk=3)
        self.assertEquals(category.__str__(), f'--{category.name}')


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        c = Category.objects.create(name='test_category', depth='1')
        author = get_user_model().objects.create(email='test_category@bk.ru', password='1')
        Article.objects.create(name='test_article', category=c, descr='test_descr', content='test_content',
                               author=author, slug='test_article', )

    def test_author_create(self):
        article = Article.objects.get(pk=1)
        author = get_user_model().objects.get(pk=1)
        field_label = article.author
        self.assertEquals(field_label, author)

    def test_name_label(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_descr_label(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('descr').verbose_name
        self.assertEquals(field_label, 'Краткое описание')

    def test_content_label(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Контент')

    def test_autocreate_slug(self):
        article = Article.objects.get(pk=1)
        field_label = article.slug
        self.assertIsNotNone(field_label)

    def test_autocreate_date_created(self):
        article = Article.objects.get(pk=1)
        field_label = article.date_created
        self.assertIsNotNone(field_label)

    def test_autocreate_date_edit(self):
        article = Article.objects.get(pk=1)
        field_label = article.date_edit
        self.assertIsNotNone(field_label)

    def test_default_likes_count(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('likes_count').default
        self.assertEquals(field_label, 0)

    def test_default_comments_count(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('comments_count').default
        self.assertEquals(field_label, 0)

    def test_default_rating(self):
        article = Article.objects.get(pk=1)
        field_label = article._meta.get_field('rating').default
        self.assertEquals(field_label, 0)

    def test_name_max_length(self):
        article = Article.objects.get(pk=1)
        max_length = article._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        article = Article.objects.get(pk=1)
        self.assertEquals(article.get_absolute_url(), f'/ru/{str(article.slug)}/detail/')

    def test__str__(self):
        article = Article.objects.get(pk=1)
        self.assertEquals(article.__str__(), f'{article.name}')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category', depth='1')
        author = get_user_model().objects.create(email='test_category@bk.ru', password='1')
        article = Article.objects.create(name='test_article', category=category, descr='test_descr',
                                         content='test_content', author=author)

        Comment.objects.create(article=article, author=author, status='P', rating='5', text='test_text').save()

    def test_author_create(self):
        comment = Comment.objects.get(pk=1)
        author = get_user_model().objects.get(pk=1)
        field_label = comment.author
        self.assertEquals(field_label, author)

    def test_name_label(self):
        comment = Comment.objects.get(pk=1)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Контент')

    def test_autocreate_date_created(self):
        comment = Comment.objects.get(pk=1)
        field_label = comment.date_created
        self.assertIsNotNone(field_label)

    def test_autocreate_date_edit(self):
        comment = Comment.objects.get(pk=1)
        field_label = comment.date_edit
        self.assertIsNotNone(field_label)

    def test_name_max_length(self):
        comment = Comment.objects.get(pk=1)
        max_length = comment._meta.get_field('status').max_length
        self.assertEquals(max_length, 100)

    def test_save_comments_count(self):
        article = Article.objects.get(pk=1)
        field_label = article.comments_count
        self.assertEquals(field_label, 1)

    def test_save_rating(self):
        article = Article.objects.get(pk=1)
        comment = Comment.objects.get(pk=1)
        rating_article = article.rating
        rating_comment = comment.rating
        self.assertEquals(float(rating_comment), float(rating_article))


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(email='test_user', password='1',
                                        img='/media/82e7d0d7-9135-4f0d-8ba6-c729cb5875d3_B0M2aBp.jpeg')
        get_user_model().objects.create(email='test_user1', password='1', )

    def test__str__(self):
        user = get_user_model().objects.get(pk=1)
        field_label = user.email
        str_user = user.__str__()
        self.assertEquals(field_label, str_user)

    def test_get_photo_url(self):
        user = get_user_model().objects.get(pk=1)
        field_label = user.get_photo_url
        self.assertEquals(field_label, '/media/media/82e7d0d7-9135-4f0d-8ba6-c729cb5875d3_B0M2aBp.jpeg')

    def test_get_photo_url_default_img(self):
        user = get_user_model().objects.get(pk=2)
        field_label = user.get_photo_url
        self.assertEquals(field_label, '/media/user.png')

    def test_get_absolute_url(self):
        user = get_user_model().objects.get(pk=1)
        field_label = user.get_absolute_url()
        self.assertEquals(field_label, '/ru/profile/')

    def test_email_user(self):
        user = get_user_model().objects.get(pk=1)
        field_label = user.email_user('subject', 'message', 'from_email')
        self.assertIsNone(field_label)


class ImageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Image.objects.create(img='/media/82e7d0d7-9135-4f0d-8ba6-c729cb5875d3_B0M2aBp.jpeg', alt='asdas')

    def test_image_url(self):
        img = Image.objects.get(pk=1)
        self.assertEquals('/media/media/82e7d0d7-9135-4f0d-8ba6-c729cb5875d3_B0M2aBp.jpeg', img.image_url)
