import statistics

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy
from treebeard.mp_tree import MP_Node

from apps.blogapp.task import send_email
from blg.utils import from_cyrillic_to_eng
from const import statusl, ratingl


class Category(MP_Node):
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name='Slug', null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']

    def __str__(self):
        if self.depth == 1:
            return self.name
        if self.depth == 2:
            return f"-{self.name}"
        else:
            return f"--{self.name}"

    def save(self, *args, **kwargs):
        """
        Добавляет слаг
        """
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает юрл главной страницы с фильтром категории
        """
        return f"/?author=&category={self.pk}&name=&o="


class Article(models.Model):
    """
    Модель поста
    """
    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name=ugettext_lazy('Slug'), null=True, blank=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Автор'),
                               null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Категория'),
                                 null=True)
    preview = models.ImageField(blank=True, null=True, verbose_name=ugettext_lazy('Превью'), default=None)
    descr = models.CharField(max_length=255, verbose_name=ugettext_lazy('Краткое описание'))
    content = RichTextUploadingField(verbose_name=ugettext_lazy('Контент'))
    favourites = models.ManyToManyField(to=get_user_model(), related_name='favourites', default=None, blank=True)
    rating = models.CharField(default=0, max_length=255, verbose_name=ugettext_lazy('Средний рейтинг'))
    comments_count = models.IntegerField(default=0, verbose_name=ugettext_lazy('Количество отзывов'))
    likes_count = models.IntegerField(default=0, verbose_name=ugettext_lazy('Количество лайков'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Дата создания'))
    date_edit = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Дата обновления'))
    recommended = models.ManyToManyField(blank=True, to='Article', related_name='recommendation',
                                         verbose_name=ugettext_lazy('Рекомендуемые статьи'))
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Добавляет слаг
        """
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        send_email.delay(self.author.pk, str(str(Site.objects.get_current()) + reverse_lazy('blogapp:detail', kwargs={
            'slug': str(self.slug)})))  # TODO: вызывается при изменении likes_count,comments_count,rating и т.д
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает юрл информации о посте
        """
        return reverse('blogapp:detail', args=[str(self.slug)])


class Image(models.Model):
    """
    Модель картинки поста
    """
    img = models.ImageField(verbose_name=ugettext_lazy('Дополнительные фото'), default=None)
    alt = models.CharField(max_length=255, verbose_name=ugettext_lazy('Краткое описание'))
    article = models.ForeignKey(to=Article, verbose_name=ugettext_lazy('Статья'), on_delete=models.SET_NULL,
                                null=True)

    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']

    @property
    def image_url(self):
        """
        Возвращает юрл картинки,если он существует
        """
        if self.img and hasattr(self.img, 'url'):
            return self.img.url


class Comment(models.Model):
    """
    Модель комментария
    """
    author = models.ForeignKey(to=get_user_model(), verbose_name=ugettext_lazy('Автор'), on_delete=models.SET_NULL,
                               null=True)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name=ugettext_lazy('Статья'),
                                null=True)

    status = models.CharField(choices=statusl, max_length=100, verbose_name=ugettext_lazy('Статус'), default='P')

    rating = models.CharField(choices=ratingl, max_length=100, verbose_name=ugettext_lazy('Рейтинг'), null=True,
                              blank=True)
    text = RichTextField(verbose_name=ugettext_lazy('Контент'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Cчитает кол-во комментариев,средний рейтинг поста
        """
        model_class = self._meta.model
        object_list = model_class.objects.filter(article=self.article, status="P")
        if object_list:
            self.article.rating = Comment.objects.all().filter(article=self.article, status="P").aggregate(
                Avg('rating')).get('rating__avg')
            self.article.comments_count = Comment.objects.all().filter(article=self.article, status="P").count()
            self.article.save()
        super().save()
