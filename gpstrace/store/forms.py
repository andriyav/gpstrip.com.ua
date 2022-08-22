from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CheckoutForms(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Ім'я", 'class': 'form-input'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Прізвище', 'class': 'form-input'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Вулиця', 'class': 'form-input'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Місто', 'class': 'form-input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Електронна адреса', 'class': 'form-input'
    }))
    index = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': ' Індекс', 'class': 'form-input'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Телефон', 'class': 'form-input'
    }))
