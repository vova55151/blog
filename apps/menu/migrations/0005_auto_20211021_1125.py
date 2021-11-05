# Generated by Django 3.2.7 on 2021-10-21 08:25

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20211021_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, verbose_name='slug')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Контент')),
                ('status', models.BooleanField(choices=[(False, 'Draft'), (True, 'Published')], default=True, null=True, verbose_name='Статус')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='menu',
            name='show',
            field=models.BooleanField(choices=[(False, 'Отображать'), (True, 'Не отображать')], verbose_name='Отображать'),
        ),
    ]
