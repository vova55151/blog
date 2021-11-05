from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy
from django_unique_slugify import unique_slugify
from slugify import slugify

from const import targets, posl


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Название'))
    url = models.CharField(max_length=200, verbose_name=ugettext_lazy('URL'))

    target = models.CharField(choices=targets, max_length=20, verbose_name=ugettext_lazy('Target'),
                              default="_self")
    pos = models.CharField(choices=posl, max_length=20, verbose_name=ugettext_lazy('Позиция меню'))
    show = models.BooleanField(verbose_name=ugettext_lazy('Отображать'),
                               choices=((True, ugettext_lazy('Отображать')), (False, ugettext_lazy('Не отображать'))))
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']


class TextPage(models.Model):
    title = models.CharField(verbose_name=ugettext_lazy('Заголовок'), max_length=50)
    slug = models.SlugField(verbose_name=ugettext_lazy('slug'), blank=True)
    content = RichTextUploadingField(verbose_name=ugettext_lazy('Контент'))
    status = models.BooleanField(verbose_name=ugettext_lazy('Статус'), choices=((False, 'Draft'), (True, 'Published')),
                                 default=True, null=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Добавляет слаг
        """
        if not self.slug:
            unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:text_page', kwargs={'slug': self.slug})
