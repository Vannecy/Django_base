from django.shortcuts import render, redirect
from .forms import NewUserForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
        users = User.objects.all()  # Récupérer tous les utilisateurs
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if user_ip:
        # Séparez les adresses IP si elles sont fournies sous forme de liste
            user_ip = user_ip.split(',')[0].strip()
        else:
            user_ip = request.META.get('REMOTE_ADDR', None)
        return render(request, 'index.html', {'users': users,'user_ip': user_ip})


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
                return redirect('authentification:index')
            else:
                message = 'Login failed!'
    return render(request, 'login.html', context={'form': form, 'message': message})


@login_required
def user_logout(request):
    logout(request)
    return redirect('authentification:index')

