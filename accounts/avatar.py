from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models

from PIL import Image


@login_required
def set_avatar(request):
    """Set or edit the avatar image."""
    user = request.user
    avatar_form = forms.AvatarForm()
    if request.method == 'POST':
        try:
            user.profile = request.user.profile  # Set Profile instance for the current user
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)  # Set the Profile instance for new user
        avatar_form = forms.AvatarForm(data=request.POST, files=request.FILES, instance=user.profile)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request,
                             "Avatar uploaded successully."
                             )
        return HttpResponseRedirect(reverse('accounts:set_avavtar'))

    return render(request, 'accounts/set_avatar.html', {
        'current_user': user,
        'avatar_form': avatar_form,
    })


@login_required
def rotate_90_cc(request):
    click = 0

    """Rotate the image 90deg counter-clockwise."""
    user = request.user
    user.profile = request.user.profile
    avatar_form = forms.AvatarForm()

    if click >= 0:
        click += 1

    avatar = Image.open(user.profile.avatar)

    avatar_90_cc = '/{0}/{1}/{2}'.format('avatars', user, 'rotated_90_cc.jpg')
    tmp_file = settings.MEDIA_ROOT + avatar_90_cc
    avatar.rotate(click*90, resample=3, expand=True).save(tmp_file)

    return render(request, 'accounts/set_avatar.html', {
        'current_user': user,
        'avatar_form': avatar_form,
        'avatar_90_cc': avatar_90_cc,
    })
