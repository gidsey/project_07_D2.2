from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = models.Profile(user=user)
        profile.save()


post_save.connect(save_profile, sender=User)