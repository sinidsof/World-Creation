from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .validators import validate_username, validate_password
from .models import CustomUser
from django import forms


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


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Роля"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)  # Извикваме валидатора за потребителското име
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)  # Извикваме валидатора за паролата
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', 'Паролите не съвпадат.')

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
