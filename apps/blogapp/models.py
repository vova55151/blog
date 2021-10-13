import statistics

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils.translation import ugettext_lazy
from treebeard.mp_tree import MP_Node

from blg.utils import from_cyrillic_to_eng


class Category(MP_Node):
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name='Slug', null=True, blank=True)

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
        return f"/blog/?author=&category={self.pk}&name=&o="


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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Добавляет слаг
        """
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
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
    img = models.ImageField(blank=True, null=True, verbose_name=ugettext_lazy('Дополнительные фото'), default=None)
    alt = models.CharField(max_length=255, verbose_name=ugettext_lazy('Краткое описание'))
    article = models.ForeignKey(to=Article, verbose_name=ugettext_lazy('Статья'), on_delete=models.SET_NULL,
                                null=True)


class Comment(models.Model):
    """
    Модель комментария
    """
    author = models.ForeignKey(to=get_user_model(), verbose_name=ugettext_lazy('Автор'), on_delete=models.SET_NULL,
                               null=True)
    article = models.ForeignKey(to=Article, on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Статья'),
                                null=True)

    statusl = (
        ('D', 'Draft'),
        ('P', 'Published'),

    )
    status = models.CharField(choices=statusl, max_length=100, verbose_name=ugettext_lazy('Статус'))
    ratingl = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.CharField(choices=ratingl, max_length=100, verbose_name=ugettext_lazy('Рейтинг'), null=True,
                              blank=True)
    text = RichTextField(verbose_name=ugettext_lazy('Контент'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Добавляет слаг,считает кол-во комментариев,средний рейтинг поста
        """
        model_class = self._meta.model
        # if model_class.objects.filter(author=self.author, article=self.article).exists():
        #     print(model_class.objects.filter(author=self.author, article=self.article).exists())
        # print(model_class.objects.filter(author=self.author, article=self.article, status="P").exists())

        #     .annotate(Count('rating'))
        # self.objects.article.comments_count = count.comment_rating__count

        object_list = model_class.objects.filter(article=self.article, status="P")  # .exclude(author=self.author)
        if object_list:
            self.article.rating = Comment.objects.all().filter(article=self.article, status="P").aggregate(
                Avg('rating')).get('rating__avg')
            self.article.comments_count = Comment.objects.all().filter(article=self.article, status="P").count()
            self.article.save()
        super().save()


# class TextPage(models.Model):
#     """
#     ???
#     """
#     name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Название'))
#     slug = models.SlugField(unique=True)
#     statusl = [
#         ('D', 'Draft'),
#         ('P', 'Published')
#     ]
#     status = models.CharField(choices=statusl, max_length=255,
#                               verbose_name=ugettext_lazy('Статус обращения'))  # Селект Draft Published
#
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_edit = models.DateTimeField(auto_now=True)
