from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from cart.cart import Cart
from store.models import Item, Category, OrderItem, Order, Favorite




def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

# Create your views here.
def add_to_cart(request, item_slug):
    if request.user.is_authenticated:
        try:
            order_qty = request.GET["order-qty"]
        except:
            order_qty = 1
        item = get_object_or_404(Item, slug=item_slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += int(order_qty)
                order_item.save()
                messages.info(request, "Кількість товару в корзині збільшена")
                return redirect("index")
            else:
                order.items.add(order_item)
                order_item.quantity = int(order_qty)
                order_item.save()
                messages.info(request, "Товар добавлено до корзини")
                return redirect("index")
        else:
            # ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user)
            order.items.add(order_item)
            messages.info(request, "Товар добавлено до корзини")
            return redirect("index")

    else:
        cart = Cart(request)
        try:
            order_qty = int(request.GET["order-qty"])
        except:
            order_qty = 1
        item = get_object_or_404(Item, slug=item_slug)
        cart.add(item=item, qty=order_qty)
        return redirect("index")

def remove_from_cart(request, item_slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=item_slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "Товар було видалено з корзини")
                return redirect("cart")
            else:
                messages.info(request, "Товар відсутній в корзині")
                return redirect("cart")
        else:
            messages.info(request, "У вас не має активних замовлень")
            return redirect("cart")
    else:
        cart = Cart(request)
        item = get_object_or_404(Item, slug=item_slug)
        cart.delete(item=item)
        return redirect("index")

