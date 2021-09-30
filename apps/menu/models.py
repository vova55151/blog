from django.db import models


# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.CharField(max_length=200, verbose_name='URL')
    targets = [

        ('B', '_blank'),
        ('S', '_self')
    ]
    target = models.CharField(choices=targets, max_length=20, verbose_name='Target',
                              default="_self")
    posl = [
        ('H', 'Header'),
        ('F', 'Footer')
    ]
    pos = models.CharField(choices=posl, max_length=20, verbose_name='Позиция меню')

