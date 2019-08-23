"""Account Models"""

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    """Define the Profile Model (linked to the User Model)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    # date_of_birth = models.DateField(null=True)
    # bio = models.TextField(null=True)
    # avatar = models.ImageField(upload_to=user_directory_path, max_length=255, null=True)
    # county = models.CharField(max_length=255, null=True)
    # interests = models.TextField(null=True)
    # website = models.URLField(null=True)

#  Extending User model reference from Simple is Better than Complex:
#  https://tinyurl.com/h4jzwop

#


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)




