from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from apps.accounts.admin import CustomUserManager
from django.utils.translation import ugettext_lazy


class User(AbstractUser):
    """
    Переопределенная модель юзера ,использующая Email вместо юзернейма для логина
    Атрибуты:
    is_manager(bool): проверка,является ли юзер менеджером
    img: Фото профиля
    """
    # many to many field (to="self")
    username = None
    phone = models.CharField(max_length=100, verbose_name='Телефон', blank=True, null=True)
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    img = models.ImageField(blank=True, null=True, verbose_name='Фото профиля')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Строковое представление юзера
        Возвращает email юзера
        """
        return self.email
