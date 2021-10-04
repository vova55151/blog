# Generated by Django 3.2.7 on 2021-09-28 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0008_auto_20210928_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='img',
        ),
        migrations.RemoveField(
            model_name='article',
            name='imgalt',
        ),
        migrations.AddField(
            model_name='category',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.article', verbose_name='Статья'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.article', verbose_name='Статья'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото профиля')),
                ('alt', models.CharField(max_length=255, verbose_name='Краткое описание')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.article', verbose_name='Статья')),
            ],
        ),
    ]