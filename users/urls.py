from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.user_signin_signup, name='signin'),
    path('signout', views.user_signout, name='signout'),
    path('user/<int:pk>/edit-profile', views.edit_user_profile, name='edit_user_profile'),
]