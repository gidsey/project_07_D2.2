# Generated by Django 2.2.4 on 2019-09-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20190910_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(help_text='Required. Min 10 characters', null=True),
        ),
    ]
