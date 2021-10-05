from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse

from apps.accounts.admin import CustomUserManager
from django.utils.translation import ugettext_lazy


class User(AbstractUser):
    """
    Переопределенная модель юзера ,использующая Email вместо юзернейма для логина
    Атрибуты:
    is_manager(bool): проверка,является ли юзер менеджером
    img: Фото профиля
    """
    username = None
    subscribers = models.ManyToManyField(to="self", related_name='subscribers', default=None, blank=True)
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

    @property
    def get_photo_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        else:
            return "/media/user.png"

    def get_absolute_url(self):
        """
        Возвращает юрл информации о компанни с определенным pk
        """
        return reverse('accounts:profile', args=[int(self.pk)])
