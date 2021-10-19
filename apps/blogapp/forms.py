from django import forms
import re

from django.forms import inlineformset_factory

from apps.blogapp.models import *


class ArticleModelForm(forms.ModelForm):
    """
    Модельная форма поста
    """

    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview', 'comments_count', 'likes_count']


    def clean_name(self):
        """
        Вызывается при отправке формы.Проверяет ,есть ли аналогичное название поста в БД
        Возвращает ValidationError,если форма не валидна
        """
        name = self.cleaned_data['name']
        qs = Article.objects.filter(name__iexact=name)
        if self.instance is not None:
            qs = qs.exclude(slug=self.instance.slug)
        if qs.exists():
            raise forms.ValidationError("Введите уникальное название")
        return name

    def clean_slug(self):
        """
        Проверяет ,есть ли аналогичный slug в БД
        Возвращает ValidationError,если форма не валидна
        """
        slug = self.cleaned_data['slug']
        qs = Article.objects.filter(slug__iexact=slug)
        if self.instance is not None:
            qs = qs.exclude(slug=self.instance.slug)
        if qs.exists():
            raise forms.ValidationError("Введите уникальное название")
        return slug


class CommentModelForm(forms.ModelForm):
    """
    Модельная форма комментария
    """

    class Meta:
        model = Comment
        fields = ['text', 'status', 'rating']


class ImgModelForm(forms.ModelForm):
    """
    Модельная форма фото
    """

    class Meta:
        model = Image
        fields = ['img', 'alt', 'article']


Img_inline = inlineformset_factory(Article,
                                   Image,
                                   fields=['img', 'alt', 'article'],
                                   form=ImgModelForm,
                                   extra=1, )
