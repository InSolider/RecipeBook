from django.db import transaction
from django.contrib import messages
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CustomRegistrationForm, EditProfileForm, EditEmailForm, ChangePasswordForm

def user_signin_signup(request):
    if request.POST.get('submit') == 'sign-in':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('next') != '':
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.info(request, 'Неправильний логін або пароль.')
            return redirect('signin')

    elif request.POST.get('submit') == 'sign-up':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            newuser = authenticate(username = username, password = password)
            login(request, newuser)
            return redirect('home')
        else:
            return render(request,'users/signin.html', {'form': form})

    else:
        return render(request, 'users/signin.html', {})

def user_signout(request):
    logout(request)
    return redirect('home')

# View for editing user profile

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile_form = EditProfileForm(instance=request.user.profile)
        return render(request, 'users/edit_profile.html', {'profile_form': profile_form})
    
    @transaction.atomic
    def post(self, request, pk):
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Інформація у профілі успішно оновлена!'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, _('Введено некоректні дані!'))
        return render(request, 'users/edit_profile.html', {'profile_form': profile_form})

# View for editing user email

class EditEmailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        email_form = EditEmailForm(instance=request.user)
        return render(request, 'users/edit_email.html', {'email_form': email_form})

    @transaction.atomic
    def post(self, request, pk):
        email_form = EditEmailForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, _('Налаштування були успішно оновлені!'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, _('Введено некоректні дані!'))
        return render(request, 'users/edit_email.html', {'email_form': email_form})

# View for changing user password

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    @transaction.atomic
    def post(self, request, pk):
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, _('Пароль успішно змінено!'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, _('Введено неправильний старий пароль або новий не відповідає вимогам!'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request, 'users/change_password.html', {})