from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm, UserEditForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .models import UserBase
from django.contrib.auth.decorators import login_required
from store.models import Item,  OrderItem, Order
from cart.cart import Cart
from django.utils import timezone
from django.contrib import messages

@login_required
def dashboard(request):
    cart = Cart(request)
    for item_cart in cart:
        item = Item.objects.get(slug=item_cart['slug'])
        order_item, created = OrderItem.objects.get_or_create(user=request.user,  item=item)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        print(order_item.quantity,'order_qty')
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity = item_cart['qty']
                order_item.save()
                messages.info(request, "Кількість товару в корзині збільшена1")
                # return redirect("index")
            else:
                order.items.add(order_item)
                order_item.quantity = item_cart['qty']
                order_item.save()
                messages.info(request, "Товар добавлено до корзини1")
                # return redirect("index")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "Товар добавлено до корзини2")
    request.session['skey'] = {}
    request.session.modified = True
    orders = Order.objects.filter(user=request.user).filter(ordered=True)
    return render(request, 'account/user/dashboard.html', {'orders': orders})

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


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
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')



