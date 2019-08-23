from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


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
    form = UserCreationForm()
    user_form = forms.UserForm()
    profile_form = forms.ProfileForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            user_form = forms.UserForm(data=request.POST, instance=current_user)
            profile_form = forms.ProfileForm(data=request.POST, instance=current_user)
            if user_form.is_valid() and profile_form.is_valid():
                current_user.save()
                user_form.save()
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
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile

    return render(request, 'accounts/sign_up.html', {
        'user_form': user_form,
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

