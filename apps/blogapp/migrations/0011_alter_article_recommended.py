# Generated by Django 3.2.7 on 2021-10-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0010_alter_article_recommended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='recommended',
            field=models.ManyToManyField(blank=True, related_name='recommendation', to='blogapp.Article', verbose_name='Рекомендуемые статьи'),
        ),
    ]
