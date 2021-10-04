import statistics

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy

from blg.utils import from_cyrillic_to_eng


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name='Slug', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))

        super().save(*args, **kwargs)


# TODO : категория и подкатегория к статье many to many or fk

class Subcategory(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Категория'),
                                 null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name='Slug', null=True, blank=True)
    parents = [
        ('H', 'Header'),
        ('F', 'Footer')
    ]
    parent = models.CharField(choices=parents, max_length=20, verbose_name='Родитель')  # TODO : ?

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))

        super().save(*args, **kwargs)


class Article(models.Model):
    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True, verbose_name=ugettext_lazy('Slug'), null=True, blank=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Автор'),
                               null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Категория'),
                                 null=True)
    preview = models.ImageField(blank=True, null=True, verbose_name=ugettext_lazy('Превью'), default=None)
    subcategory = models.ForeignKey(to=Subcategory, on_delete=models.SET_NULL,
                                    verbose_name=ugettext_lazy('Подкатегория'),
                                    null=True)
    descr = models.CharField(max_length=255, verbose_name=ugettext_lazy('Краткое описание'))
    content = RichTextField(verbose_name=ugettext_lazy('Контент'))
    recl = [
        ('H', 'Header'),
        ('F', 'Footer'),
    ]
    rec = models.CharField(choices=recl, max_length=255,
                           verbose_name=ugettext_lazy('Рекомендуемые статьи'))  # TODO :нету
    favourites = models.ManyToManyField(to=get_user_model(), related_name='favourites', default=None, blank=True)
    rating = models.CharField(max_length=255, verbose_name=ugettext_lazy('Средний рейтинг'))
    comments_count = models.CharField(max_length=255, verbose_name=ugettext_lazy('Количество отзывов'))
    likes_count = models.CharField(max_length=255, verbose_name=ugettext_lazy('Количество лайков'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Дата создания'))
    date_edit = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Дата обновления'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            if Article.objects.filter(slug=self.slug).count() > 0:
                self.slug = from_cyrillic_to_eng(str(f'{self.name}_{self.author}'))

        # self.comments_count = self.comment_set.all().count()# v comment
        # self.likes_count = self.like_set.all().count()# v like
        # self.rating_average = self.comment_set.aggregate()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает юрл информации о компанни с определенным pk
        """
        return reverse('blogapp:detail', args=[str(self.slug)])


class Image(models.Model):
    img = models.ImageField(blank=True, null=True, verbose_name=ugettext_lazy('Дополнительные фото'), default=None)
    alt = models.CharField(max_length=255, verbose_name=ugettext_lazy('Краткое описание'))
    article = models.ForeignKey(to=Article, verbose_name=ugettext_lazy('Статья'), on_delete=models.SET_NULL,
                                null=True)


class Comment(models.Model):
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
    rating = models.CharField(choices=ratingl, max_length=100, verbose_name=ugettext_lazy('Рейтинг'))
    text = RichTextField(verbose_name=ugettext_lazy('Контент'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        model_class = self._meta.model
        # if model_class.objects.filter(author=self.author, article=self.article).exists(): #TODO : проверка не работает
        #     print(model_class.objects.filter(author=self.author, article=self.article).exists())
        object_list = model_class.objects.filter(article=self.article)  # .exclude(author=self.author)
        print(model_class.objects.filter(author=self.author, article=self.article).exists())
        if object_list:
            self.article.rating = statistics.mean([int(i.rating) for i in object_list])
            self.article.save()
        super().save()

#
# class Like(models.Model):
#     author = models.ForeignKey(to=get_user_model(), verbose_name=ugettext_lazy('Автор'), on_delete=models.SET_NULL,
#                                null=True)
#     article = models.ForeignKey(to=Article, on_delete=models.SET_NULL, verbose_name=ugettext_lazy('Статья'),
#                                 null=True)


class TextPage(models.Model):
    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Название'))
    slug = models.SlugField(unique=True)
    statusl = [
        ('D', 'Draft'),
        ('P', 'Published')
    ]
    status = models.CharField(choices=statusl, max_length=255,
                              verbose_name=ugettext_lazy('Статус обращения'))  # Селект Draft Published

    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
