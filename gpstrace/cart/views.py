from django.shortcuts import render


def cart_summary(request):
    return render(request, 'cart/cart.html')

# Create your views here.
