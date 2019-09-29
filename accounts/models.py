"""Account Models"""
from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/avatars/user/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    """Define the Profile Model (linked to the User Model)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()  # Required field
    bio = models.TextField(help_text='Minimum 10 characters')  # Required field
    avatar = models.ImageField(
        upload_to=user_directory_path,
        max_length=255,
        null=True,
        blank=True,
        default='placeholder/default.png',
    )  # Optional field
    city = models.CharField(max_length=100)  # Required field
    county = models.CharField(max_length=255, blank=True)  # Optional field
    country = models.CharField(max_length=100)  # Required field
    interests = models.TextField(blank=True)  # Optional field
    website = models.URLField(blank=True,)  # Optional field

