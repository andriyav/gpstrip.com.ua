


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


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())