from django import template
from ..models import Category, Item, Order, OrderItem, Favorite, ONE_HUNDRED, FIVE_HUNDRED, TEN_HUNDRED, TWENTY_HUNDRED
from feedback.models import Feedback


register = template.Library()

#
# @register.simple_tag()
# def get_labeled(filter='Популярне'):
#     if not filter:
#         return Item.objects.all()
#     else:
#         return Item.objects.filter(label=filter)


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
        qs = Order.objects.filter(user=user, ordered=False).select_related('user')
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def get_cart_navbar(user):
    if user.is_authenticated:
        cart_item = OrderItem.objects.filter(user=user, ordered=False).select_related('item')
        if cart_item.exists():
            return cart_item

@register.filter
def get_favorite(user):
    if user.is_authenticated:
        favorite_item = Favorite.objects.filter(user=user).select_related('item_favorite')
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
        qs_order_item = OrderItem.objects.filter(user=user, ordered=False).select_related("item")
        for prices in qs_order_item:
            if prices.item.discount:
                total_item = prices.quantity * (prices.item.price - (
                            prices.item.price * (prices.item.discount / 100)))
            else:
                total_item = prices.quantity * prices.item.price
            total += total_item
    return total

@register.filter
def favorite_item_count(user):
    if user.is_authenticated:
        qs = Favorite.objects.filter(user=user).select_related("user_id")
        if qs.exists():
            return qs.count()
    return 0

@register.inclusion_tag('store/list_viewed.html')
def get_viewed(slug):
    item_viewed = Item.objects.filter(slug__in=slug).select_related('cat')
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

@register.inclusion_tag('feedback/feedback.html')
def get_feedback(slug):
    feedback = Feedback.objects.filter(slug=slug)
    return {'feedback': feedback}

@register.filter
def feedback_count(slug):
    fd = Feedback.objects.filter(slug=slug)
    if fd.exists():
        return fd.count()
    return 0


@register.filter
def feedback_sum_rate(slug):
    fd = Feedback.objects.filter(slug=slug)
    return fd.count()

@register.filter
def feedback_average_rate(slug):
    fd = Feedback.objects.filter(slug=slug)
    sum_rate = 0
    feed_c = feedback_count(slug)
    for rate_num in fd:
        sum_rate += int(rate_num.rate)
    if feed_c == 0:
        return 0
    else:
        return sum_rate/feed_c

@register.filter
def feedback_rate_qty(slug, rate):
    fd = Feedback.objects.filter(slug=slug, rate=rate)
    if fd.exists():
        return fd.count()
    return 0

@register.filter
def feedback_rate_percentage(slug, rate):
    if feedback_sum_rate(slug) == 0:
        return 0
    else:
        return feedback_rate_qty(slug, rate) * 100/feedback_sum_rate(slug)


