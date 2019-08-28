from django.urls import path

from . import views

app_name = "accounts"  # required when using namespace in URLS

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile_only', views.profile_only, name='profile_only'),  # Test Profile URL (can be removed)
]
