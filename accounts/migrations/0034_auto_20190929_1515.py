# Generated by Django 2.2.4 on 2019-09-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20190929_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='---', help_text='Minimum 10 characters'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
    ]
