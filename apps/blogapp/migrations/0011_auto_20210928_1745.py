# Generated by Django 3.2.7 on 2021-09-28 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0010_auto_20210928_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='article',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.subcategory', verbose_name='Подкатегория'),
        ),
    ]
