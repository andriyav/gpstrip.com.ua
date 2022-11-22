from django.shortcuts import render, redirect

from .forms import RegistrationForm

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
            message = render('account/registration/account_activaion_email.html',
                             'user': user,
                            'domain': current_site.domian
            )

