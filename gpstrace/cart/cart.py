from decimal import Decimal
import json
import jsonpickle
from json import JSONEncoder
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
        if item_slug in self.cart:
            self.cart[item_slug]['qty'] = qty
        else:
            self.cart[item_slug] = {'price': int(item.price), 'qty': int(qty)}
        self.session.modified = True

    def __iter__(self):
        item_slugs = self.cart.keys()
        items = Item.objects.filter(slug__in=item_slugs)
        cart = self.cart.copy()
        for item_s in items:
            cart[item_s.slug]['title'] = str(item_s.title)
            cart[item_s.slug]['photo'] = 'static/' + str(item_s.photo)
            cart[item_s.slug]['discount'] = item_s.discount
            cart[item_s.slug]['slug'] = str(item_s.slug)
        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['qty'])

            yield item




    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) - (Decimal(item['price']) * ((Decimal(item['discount'])/ 100)))
                   * item['qty'] for item in self.cart.values() if item['discount'])

    def discount_price_calculation(self):
        for item in self.cart.values():
            if item['discount']:
                self.discount_price = Decimal(item['price']) - (Decimal(item['price']) * ((Decimal(item['discount'])/ 100)))

        return self.discount_price

    def delete(self, item):
        item_slug = item.slug
        if item_slug in self.cart:
            del self.cart[item_slug]
            self.session.modified = True


