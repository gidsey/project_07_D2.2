"""Account Models"""
import os
from django.db import models
from django.contrib.auth.models import User
import datetime


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/avatars/user/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    """Define the Profile Model (linked to the User Model)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    verify_email = models.EmailField(label="Please verify your email address")
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to=user_directory_path, max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    interests = models.TextField(null=True)
    website = models.URLField(null=True)


    def clean(self):
        """Clean the entire form"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')  # Or cleaned_data['email']
        verify = cleaned_data.get('verify_email')
        date_of_birth = cleaned_data.get('date_of_birth')

        if email != verify:
            raise models.ValidationError(
                "Emails do not match"
            )


        if date_of_birth != datetime:
            raise models.ValidationError(
                "Please enter a valid date"
            )




