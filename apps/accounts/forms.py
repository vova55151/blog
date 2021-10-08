from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
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

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img']
