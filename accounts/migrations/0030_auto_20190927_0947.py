# Generated by Django 2.2.4 on 2019-09-27 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_profile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
