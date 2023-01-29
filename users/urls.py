from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.login_user, name='signin'),
]