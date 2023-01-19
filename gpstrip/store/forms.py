from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CheckoutForms(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Ім'я", 'class': "input"
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Прізвище', 'class': "input"
    }))
    street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Вулиця', 'class': "input"
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Місто', 'class': "input"
    }))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Електронна адреса', 'class': "input"
    }))
    index = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': ' Індекс', 'class': "input"
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон', 'class': "input"
    }))
    city_np = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон', 'class': "input"
    }))
    first_name_np = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Ім'я", 'class': "input"
    }))
    last_name_np = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Прізвище', 'class': "input"
    }))
    address_np = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Вулиця', 'class': "input"
    }))
    phone_np = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон', 'class': "input"
    }))
    order_notes = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Нотатки до замовлення', 'class': "input"
    }))


