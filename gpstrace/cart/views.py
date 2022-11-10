from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from cart.cart import Cart
from store.models import Item


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

# Create your views here.
def add_to_cart(request, item_slug):
    cart = Cart(request)
    try:
        order_qty = int(request.GET["order-qty"])
    except:
        order_qty = 1
    item = get_object_or_404(Item, slug=item_slug)
    cart.add(item=item, qty=order_qty)
    return redirect("index")

    # if 'cart' not in request.session:
    #     request.session['cart'] = {}
    #     request.session['cart'][item_slug] = order_qty
    #     messages.info(request, "Товар добвалено до корзини")
    # else:
    #
    #     if item_slug in request.session['cart']:
    #         order_qty += int(request.session['cart'][item_slug])
    #         request.session['cart'][item_slug] = order_qty
    #     else:
    #         request.session['cart'][item_slug] = order_qty
    #         messages.info(request, "Товар добвалено до корзини")
    #
    # request.session.modified = True
    # return redirect("index")