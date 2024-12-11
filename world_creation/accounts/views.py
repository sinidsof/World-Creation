from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy



UserModel = get_user_model()
class RegisterView(FormView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user.role == 'super_creator':
            user.is_superuser = True
            user.is_staff = True
        user.save()

        messages.success(self.request, 'Успешно се регистрирахте! Можете да се логнете сега.')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


    def save(self, commit=True):
        user = super().save(commit=False)
        # Персонализирана логика, ако е необходима
        if commit:
            user.save()
        return user



class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('task_list')  # По подразбиране, ако няма роля

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Добре дошли, {user.username}!')

            # Пренасочване според ролята
            if user.role == 'super_creator':
                return redirect('super_creator_dashboard')
            return super().form_valid(form)
        else:
            messages.error(self.request, "Невалидни данни за вход. Моля, опитайте отново.")
            return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, "Моля, попълнете коректно формата.")
        return super().form_invalid(form)



def custom_logout(request):
    logout(request)  # Изход от системата
    return redirect('login')


@login_required
def profile(request):
    # Вземаме профила на текущия потребител (ако съществува)
    profile = request.user.profile  # връзка 1:1 между CustomUser и Profile
    return render(request, 'accounts/profile.html', {'user': request.user, 'profile': profile})


@login_required
def edit_profile(request):
    # Формата се променя в зависимост от ролята на потребителя
    if request.user.role == 'super_creator':
        form = UserChangeForm(request.POST or None, instance=request.user)
    else:
        form = CustomUserProfileForm(request.POST or None, instance=request.user)

    # Ако формата е валидна, записваме промените
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')  # Пренасочваме към профила на потребителя

    return render(request, 'accounts/edit_profile.html', {'form': form})





