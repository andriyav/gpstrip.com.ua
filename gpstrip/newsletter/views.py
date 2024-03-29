from django.utils import timezone

from django.shortcuts import render, redirect
from . models import Subscribers
from . forms import MessageForms
from django.core.mail import send_mail
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required

# Create your views here.

def newsletter_subscriber(request):
    if request.method == 'POST':
        print(request.POST)
        Subscribers.objects.get_or_create(email=request.POST['subscriber'])
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def message_send(request):
    if request.user.is_superuser:
        emails = Subscribers.objects.all()
        df = read_frame(emails, fieldnames=['email'])
        mail_list = df['email'].values.tolist()
        if request.method == 'POST':
            form = MessageForms(request.POST)
            if form.is_valid():
                form.save()
                title = form.cleaned_data.get('title')
                message = form.cleaned_data.get('message')
                send_mail(
                    title,
                    message,
                    '',
                    mail_list,
                    fail_silently=False,
                )
                return redirect('massage-send')
        else:
            form = MessageForms()

        context = {
            'form_letter': form
        }
        return render(request, 'newsletter/news_letter.html', context)
    else:
        print('у Вас не має прав')
        return redirect('home')


