from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomRegistrationForm

def user_signin_signup(request):
    if request.POST.get('submit') == 'sign-in':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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