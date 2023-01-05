from django import forms
from . models import Subscribers, MailMessage

class MessageForms(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'
