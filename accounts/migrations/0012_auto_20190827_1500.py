# Generated by Django 2.2.4 on 2019-08-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190827_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='verify_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
