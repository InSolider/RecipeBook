from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.user_signin_signup, name='signin'),
    path('signout', views.user_signout, name='signout'),
]