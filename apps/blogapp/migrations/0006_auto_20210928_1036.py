# Generated by Django 3.2.7 on 2021-09-28 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_alter_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug'),
        ),
    ]