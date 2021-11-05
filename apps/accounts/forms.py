import re

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy
from django_registration.forms import RegistrationForm

from apps.accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Переопределенная форма создания юзера
    """
    class Meta:
        model = get_user_model()
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    """
    Переопределенная форма смены юзера
    """
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()


class UserModelForm(forms.ModelForm):
    """
    Форма юзера,валидирует email и телефон
    """
    email = forms.EmailField(disabled=True, label=ugettext_lazy('Email'))
    first_name = forms.CharField(required=True, label=ugettext_lazy('Имя'))
    last_name = forms.CharField(required=True, label=ugettext_lazy('Фамилия'))
    phone = forms.CharField(required=True, label=ugettext_lazy('Телефон'))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img', 'email']

    # def clean_phone(self):
    #     """
    #     Вызывается при отправке формы.Проверяет валидность номера телефона
    #     Возвращает ValidationError,если форма не валидна
    #     """
    #     phone = self.cleaned_data.get('phone')
    #     pattern = r'^\+[0-9\-\+]{10}$'
    #     if re.match(pattern, phone):
    #         return phone
    #     else:
    #         raise forms.ValidationError("Ведите правильный номер телефона")
    #
    # def clean_email(self):
    #     email = self.instance.email
    #     return email
