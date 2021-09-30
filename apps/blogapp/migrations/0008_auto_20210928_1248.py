# Generated by Django 3.2.7 on 2021-09-28 09:48

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0007_auto_20210928_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.CharField(max_length=255, verbose_name='Средний рейтинг'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.article', verbose_name='Статья')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=255, verbose_name='Рейтинг')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Контент')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_edit', models.DateField(auto_now=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.article', verbose_name='Статья')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
