# Generated by Django 3.2.7 on 2021-10-21 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20211021_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='textpage',
            old_name='created',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='textpage',
            old_name='updated',
            new_name='date_edit',
        ),
    ]
