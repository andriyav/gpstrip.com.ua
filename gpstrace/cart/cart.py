from decimal import Decimal

from store.models import Item


class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, item, qty):
        item_slug = item.slug
        if item_slug not in self.cart:
            self.cart[item_slug] = {'price': int(item.price), 'qty': int(qty)}
        self.session.modified = True

    def __iter__(self):
        item_slugs = self.cart.keys()
        items = Item.objects.filter(slug=item_slugs)
        cart = self.cart.copy()
        for item_s in items:
            cart[item_s.slug]['item'] = item_s
        for item in cart.values():

            item['total_price'] = int(item['price']) * int(item['qty'])
            yield item


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())