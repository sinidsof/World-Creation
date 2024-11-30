from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm, CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добре дошли, {user.username}!')
                if user.role == 'super_creator':
                    return redirect('super_creator_dashboard')
                else:
                    return redirect('task_list')
            else:
                messages.error(request, "Невалидни данни за вход. Моля, опитайте отново.")
                return redirect('login')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Успешно се регистрирахте! Можете да се логнете сега.')
            return redirect('login')
        else:
            messages.error(request, 'Моля, коригирайте грешките в формата.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

"""Тази функция използва декоратора @login_required, което означава, 
че потребителят трябва да бъде влязъл, за да има достъп до страницата. 
Параметърът request.user съдържа информация за текущия логнат потребител, 
която ще предадем на шаблона."""

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


