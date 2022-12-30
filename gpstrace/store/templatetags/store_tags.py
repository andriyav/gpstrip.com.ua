from django import template
from ..models import Category, Item, Order, OrderItem, Favorite, ONE_HUNDRED, FIVE_HUNDRED, TEN_HUNDRED, TWENTY_HUNDRED

register = template.Library()


@register.simple_tag()
def get_labeled(filter='Популярне'):
    if not filter:
        return Item.objects.all()
    else:
        return Item.objects.filter(label=filter)


#

@register.inclusion_tag('store/list_discount.html')
def get_discount_30():
    item_discount = Item.objects.filter(discount='30')
    return {'item_discount': item_discount}


@register.inclusion_tag('store/list_categories.html')
def get_categories():
    cats = Category.objects.all()
    return {'cats': cats}


@register.inclusion_tag('store/list_related.html')
def get_items():
    related = Item.objects.filter(id__lte=4)
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


@register.filter
def get_cart_navbar2(order_item):
    cart_item = Item.objects.filter(slug__in=order_item)
    return cart_item


@register.filter
def get_favorite(user):
    if user.is_authenticated:
        favorite_item = Favorite.objects.filter(user=user)
        if favorite_item.exists():
            return favorite_item

@register.filter
def get_favorite_list(user):
    item_list = []
    if user.is_authenticated:
        favorite_item = Favorite.objects.filter(user=user)
        if favorite_item.exists():
            for item in favorite_item:
                item_list.append(item.item_favorite.slug)
    return item_list


@register.filter
def get_cart_total_price(user):
    total = 0

    if user.is_authenticated:
        qs_order_item = OrderItem.objects.filter(user=user, ordered=False)
        for prices in qs_order_item:
            if prices.item.discount:
                total_item = prices.quantity * (prices.item.price - (
                            prices.item.price * (prices.item.discount / 100)))
            else:
                total_item = prices.quantity * prices.item.price
            total += total_item

    return total


# self.quantity * self.item.price - (self.item.price * (self.item.discount / 100))
@register.filter
def favorite_item_count(user):
    if user.is_authenticated:
        qs = Favorite.objects.filter(user=user)
        if qs.exists():
            return qs.count()
    return 0


@register.inclusion_tag('store/list_viewed.html')
def get_viewed(slug):
    item_viewed = Item.objects.filter(slug__in=slug)
    return {'item_viewed': item_viewed}


@register.inclusion_tag('store/battery_viewed.html')
def battery_viewed(request):
    battery_viewed = [str(ONE_HUNDRED), str(FIVE_HUNDRED), str(TEN_HUNDRED), str(TWENTY_HUNDRED)]
    bat_name = request.GET
    return {'battery_viewed': battery_viewed, 'bat_name': bat_name.keys}

@register.simple_tag
def viewed(a, slug):
    try:
        a['recently_viewed']
    except:
        a['recently_viewed'] = [slug]
    else:
        if slug not in a['recently_viewed']:
            a['recently_viewed'].insert(0, slug)
    a.modified = True
    return a['recently_viewed'], slug
