# Generated by Django 2.2.4 on 2019-09-26 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20190925_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar_crop',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='avatar_crop_height',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='avatar_crop_width',
        ),
    ]
