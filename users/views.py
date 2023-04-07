from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomRegistrationForm, ProfileForm

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

@login_required
@transaction.atomic
def edit_user_profile(request, pk):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Інформація у профілі успішно оновлена!'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, _('Помилка!'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'profile_form': profile_form})
