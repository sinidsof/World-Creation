from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .validators import validate_username, validate_password
from django import forms
from .models import CustomUser, Profile

UserModel = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserModel.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Роля"
    )

    class Meta:
        model = UserModel
        fields = ('username', 'role', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)  # Валидатор за потребителското име
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)  # Валидатор за паролата
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', 'Паролите не съвпадат.')

        role = cleaned_data.get('role')

        if role == 'super_creator':
            cleaned_data['is_staff'] = True
            cleaned_data['is_superuser'] = True

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведи потребителско име'
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведи парола'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повтори паролата'
        })


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Въведи потребителско име',
            'aria-label': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Въведи парола',
            'aria-label': 'Password'
        })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Извикваме валидатора за паролата
        return password



class CustomUserProfileForm(forms.ModelForm):
    # Полета за CustomUser
    username = forms.CharField(max_length=150, label='Потребителско име')
    email = forms.EmailField(label='Имейл адрес', required=True)

    # Полета за Profile
    first_name = forms.CharField(max_length=30, required=False, label='Първо име')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Дата на раждане')
    profile_picture = forms.URLField(required=False, label='Профилна снимка')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',  'email', 'date_of_birth', 'profile_picture']

    def __init__(self, *args, **kwargs):
        # Това ще попълни полетата на формата с текущите данни от профила
        user_instance = kwargs.get('instance')
        if user_instance:
            profile = user_instance.profile
            kwargs.update({
                'initial': {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'date_of_birth': profile.date_of_birth,
                    'profile_picture': profile.profile_picture,
                }
            })
        super().__init__(*args, **kwargs)




    def save(self, commit=True):
        user = super().save(commit=False)
        # Ако има имейл, го добавяме към потребителя
        user.email = self.cleaned_data.get('email', user.email)
        if commit:
            user.save()

            # Също така актуализираме профила
            profile, created = Profile.objects.get_or_create(user=user)
            profile.first_name = self.cleaned_data['first_name']
            profile.last_name = self.cleaned_data['last_name']
            profile.date_of_birth = self.cleaned_data['date_of_birth']
            profile.profile_picture = self.cleaned_data['profile_picture']
            profile.save()

        return user

