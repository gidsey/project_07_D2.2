"""Account Models"""
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    """Define the Profile Model (linked to the User Model)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    # date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    interests = models.TextField(null=True)
    website = models.URLField(null=True)


# post_save.connect(signals.create_user_profile, sender=User)


#  Extending User model reference from Simple is Better than Complex:
#  https://tinyurl.com/h4jzwop

#


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

#
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#
#





