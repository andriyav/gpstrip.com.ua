from django import template
from ..models import Category, Item, Order, OrderItem

register = template.Library()

@register.simple_tag()
def get_labeled(filter='Популярне'):
    if not filter:
        return Item.objects.all()
    else:
        return Item.objects.filter(label=filter)


@register.inclusion_tag('store/list_categories.html')
def get_categories():
    cats = Category.objects.all()
    return {'cats': cats}


@register.inclusion_tag('store/list_related.html')
def get_items():
    related = Item.objects.filter(id__lte = 4)
    return {'related': related}


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def get_cart_navbar(user):
    if user.is_authenticated:
        cart_item = OrderItem.objects.filter(user=user, ordered=False)
        if cart_item.exists():
            return cart_item
    return 'Ваша коrзина пуста'

@register.filter
def get_cart_total_price(user):
    total = 0
    if user.is_authenticated:
        qs_order_item = OrderItem.objects.filter(user=user, ordered=False)
        if qs_order_item.exists():
            for prices in qs_order_item:
                total_item = prices.quantity * prices.item.price
                total += total_item
        return total
