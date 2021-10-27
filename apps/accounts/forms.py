import re

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy
from django_registration.forms import RegistrationForm


class CustomUserCreationForm(UserCreationForm):
    """
    Переопределенная форма создания юзера
    """

    class Meta:
        model = get_user_model()
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Переопределенная форма смены юзера
    """

    class Meta:
        model = get_user_model()
        fields = ('email',)


class UserLoginForm(forms.Form):
    email = forms.CharField(label='email', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        }))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = get_user_model().objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный пользователь неактивен')
        return super().clean(*args, **kwargs)


# class UserRegistrationForm(forms.Form):
#     email = forms.CharField(label='email', widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Введите email'
#     }))
#     password = forms.CharField(label='password', widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите password'
#         }))
#     password2 = forms.CharField(label='password', widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите password'
#         }))
#
#     class Meta:
#         model = get_user_model()
#         fields = ('email',)
#
#     def clean_password2(self):
#         data = self.cleaned_data
#         if data['password'] != data['password2']:
#             raise forms.ValidationError('Пароли не совпадают')
#         return data['password2']


class UserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()


class UserRegistrationForm(forms.Form):
    email = forms.CharField(label='email', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        }))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        }))

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UserModelForm(forms.ModelForm):
    """

    """
    email = forms.EmailField(disabled=True, label=ugettext_lazy('Email'))
    first_name = forms.CharField(required=True, label=ugettext_lazy('Имя'))
    last_name = forms.CharField(required=True, label=ugettext_lazy('Фамилия'))
    phone = forms.CharField(required=True, label=ugettext_lazy('Телефон'))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img', 'email']

    def clean_phone(self):
        """
        Вызывается при отправке формы.Проверяет валидность номера телефона
        Возвращает ValidationError,если форма не валидна
        """
        phone = self.cleaned_data.get('phone')
        pattern = r'^\+[0-9\-\+]{10}$'
        if re.match(pattern, phone):
            return phone
        else:
            raise forms.ValidationError("Ведите правильный номер телефона")

    def clean_email(self):
        email = self.instance.email
        return email
