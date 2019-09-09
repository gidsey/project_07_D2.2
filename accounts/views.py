from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import forms
from . import models


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "Account setup successully! You've been signed in too."
            )
            return HttpResponseRedirect(reverse('accounts:create_profile'))

    return render(request, 'accounts/sign_up.html', {
        'form': form,
    })


@login_required
def create_profile(request):
    """Propulate the Profile after the user has been created."""
    profile_form = forms.ProfileForm()
    user = request.user
    if request.method == 'POST':
        user.profile = models.Profile.objects.create(user=user)
        profile_form = forms.ProfileForm(data=request.POST, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request,
                "Profile saved successully."
            )
        return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/create_profile.html', {
        'profile_form': profile_form,
    })



def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='accounts/sign_in/')
def profile(request):
    """Define the Profile view"""
    user = request.user
    avatar_form = forms.AvatarForm()
    if not request.user.profile.avatar:  # Use defulat image if no avatar set
        request.user.profile.avatar = 'placeholder/default.png'

    if request.method == 'POST':
        user.profile = models.Profile.objects.get(user=user)
        avatar_form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=user.profile)
        print(request.FILES)
        if avatar_form.is_valid():
            cleaned_data = self.clean()
            avatar = cleaned_data.get('avatar')
            print('avatar = {}'.format(avatar))
            models.Profile.avatar(user=user).update(avatar=avatar)
            messages.success(
                request,
                "Avatar uploaded successully."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/profile.html', {
        'current_user': request.user,
        'avatar_form': avatar_form,
    })


@login_required(login_url='accounts/sign_in/')
def edit_profile(request):
    """Define the Edit Profile view"""
    return render(request, 'accounts/edit_profile.html', {'current_user': request.user})


@login_required(login_url='accounts/sign_in/')
def profile_only(request):
    """Test the Profile Model"""
    form = forms.ProfileForm()
    try:
        user_profile = request.user.profile  # Set Profile instance for the current user
    except models.Profile.DoesNotExist:
        user_profile = models.Profile(user=request.user)  # Set the Profile instance for new user

    if request.method == 'POST':
        form = forms.ProfileForm(data=request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'accounts/profile_only.html',
                  {'form': form, 'current_user': request.user})

