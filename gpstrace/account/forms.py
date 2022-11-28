from django import forms
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)




class RegistrationForm(forms.Form):

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)


    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Користувач з даним іменем вже існує")
        return user_name

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Паролі не однакові')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з такою електронною адресою вже зареєстрований")
        return email

