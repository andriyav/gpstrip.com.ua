from django import forms
from . models import Subscribers, MailMessage

class MessageForms(forms.ModelForm):
    title = forms.CharField(label="Тема", min_length=4, max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Тема'}))
    message = forms.CharField(label="Повідомлення", required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Повідомлення'}))
    class Meta:
        model = MailMessage
        fields = '__all__'
