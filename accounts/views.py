from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm, RegisterForm

def login_view(request):

    features = [
        'Crie e organize tarefas',
        'Prioridades e categorias',
        'Modo escuro & claro',
        'Múltiplos idiomas',
    ]

    if request.user.is_authenticated:
        return redirect('tasks:list')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Bem-vindo de volta, %(name)s!') % {'name': user.username})
            return redirect('tasks:list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, "features": features})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Conta criada com sucesso!'))
            return redirect('tasks:list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
