# Generated by Django 2.2.4 on 2019-09-27 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20190927_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=models.ImageField(default='na', upload_to=''),
            preserve_default=False,
        ),
    ]
