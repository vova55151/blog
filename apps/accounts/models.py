from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.urls import reverse

from apps.accounts.admin import CustomUserManager
from django.utils.translation import ugettext_lazy


class User(AbstractUser):
    """
    Переопределенная модель юзера ,использующая Email вместо юзернейма для логина
    """
    username = None
    subscribes = models.ManyToManyField('User', related_name='subscribers')
    phone = models.CharField(max_length=100, verbose_name=ugettext_lazy('Телефон'), blank=True, null=True)
    email = models.EmailField(verbose_name=ugettext_lazy('email address'), unique=True)
    img = models.ImageField(blank=True, null=True, verbose_name=ugettext_lazy('Фото профиля'))
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']

    def __str__(self):
        """
        Строковое представление юзера
        Возвращает email юзера
        """
        return self.email

    @property
    def get_photo_url(self):
        """
        Возвращает фото юзера,если его нет - дефолтное фото профиля
        """
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        else:
            return "/media/user.png"

    def get_absolute_url(self):
        """
        Возвращает юрл информации о пользователе
        """
        return reverse('accounts:profile')




