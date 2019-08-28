from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
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


@transaction.atomic
def sign_up(request):
    form = UserCreationForm()
    profile_form = forms.ProfileForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES)

        if form.is_valid and profile_form.is_valid():
            user = form.save()
            user.profile = models.Profile.objects.create(user=user)
            profile_form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=user.profile)
            if profile_form.is_valid():
                profile_form.save()

                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                login(request, user)
                messages.success(
                    request,
                    "You're now a user! You've been signed in, too."
                )
                return HttpResponseRedirect(reverse('accounts:profile'))

        else:  # Re-render the form with data for user to correct errors
            form = UserCreationForm(data=request.POST)
            profile_form = forms.ProfileForm(data=request.POST)

    return render(request, 'accounts/sign_up.html', {
        'form': form,
        'profile_form': profile_form
    })


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='accounts/sign_in/')
def profile(request):
    """Define the Profile view"""
    return render(request, 'accounts/profile.html', {'current_user': request.user})


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

