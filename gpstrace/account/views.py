from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes

def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = "Активуйте свій обліковий запис"
            message = render('account/registration/account_activaion_email.html', {
                             'user': user,
                            'domain': current_site.domian,
                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')
        else:
            registerForm = RegistrationForm()
        return render(request, 'account/registration/register.html', {'form': registerForm})
    #
    # def account_activate(requiest, uidb64)

