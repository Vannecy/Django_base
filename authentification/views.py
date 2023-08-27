from django.shortcuts import render, redirect
from .forms import NewUserForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def inscription(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Faites ce que vous voulez après l'inscription, par exemple, connecter l'utilisateur
            return redirect('authentification:user_login')  # Redirige vers la page d'accueil après inscription
    else:
        form = NewUserForm()
    return render(request, 'inscription.html', {'form': form})


def user_login(request):
    form = LoginForm(request.POST)
    message = 'bonjour'
    print('step1')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            print('step2')
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                print('step3')
                return redirect('gestion:home')
            else:
                message = 'Login failed!'
    return render(request, 'login.html', context={'form': form, 'message': message})


@login_required
def user_logout(request):
    logout(request)
    return redirect('gestion:home')

