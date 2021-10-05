from django import forms
import re

from django.forms import inlineformset_factory

from apps.blogapp.models import *


class ArticleModelForm(forms.ModelForm):
    """
    Модельная форма проекта
    """

    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview']

        # def clean_cost(self):
    #     """
    #     Вызывается при отправке формы.Проверяет,состоит ли стоимость только из цифр
    #     Возвращает ValidationError,если форма не валидна
    #     """
    #     cost = self.cleaned_data.get('cost')
    #     pattern = r'^[\W\d\W]*$'
    #     if re.match(pattern, cost):
    #         return cost
    #     else:
    #         raise forms.ValidationError("Стоимость должна состоять только из цифр")


class CommentModelForm(forms.ModelForm):
    """
    Модельная форма проекта
    """

    class Meta:
        model = Comment
        fields = ['text',"status",'rating']


class ImgModelForm(forms.ModelForm):
    """
    Модельная форма проекта
    """

    class Meta:
        model = Image
        fields = ['img', 'alt', 'article']


Img_inline = inlineformset_factory(Article,
                                   Image,
                                   fields=['img', 'alt', 'article'],
                                   form=ImgModelForm,
                                   extra=2,)
