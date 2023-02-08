from django.db import models
from django.urls import reverse
from django.conf import settings

LABEL_CHOICES = (
    ('Новинка', 'Новинка'),
    ('Популярне', 'Популярне'),
)

ONE_HUNDRED = 1000
FIVE_HUNDRED = 5000
TEN_HUNDRED = 10000
TWENTY_HUNDRED = 20000


BATTERY_CHOICES = (
    (ONE_HUNDRED, 1000),
    (FIVE_HUNDRED, 5000),
    (TEN_HUNDRED, 10000),
    (TWENTY_HUNDRED, 20000),

)

class Item(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='Назва товару')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to='img', null=True)
    price = models.FloatField(blank=True, null=True, verbose_name='Ціна товару')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Знижка у %')
    short_description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Короткий опис')
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Опис')
    details = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Деталі')
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True, verbose_name='Акційна мітка')
    battery = models.IntegerField(choices=BATTERY_CHOICES, null=True, blank=True,
                               verbose_name='Ємність акумуляторної батареї')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('itemv', kwargs={'item_slug': self.slug})

    def discount_price_calculation(self):
        self.discount_price = self.price - (self.price * (self.discount / 100))
        return self.discount_price

    def discount_save_calculation(self):
        self.discount_save = self.price - self.discount_price
        return self.discount_save

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'item_slug': self.slug})

    def get_add_to_favorite_url(self):
        return reverse('add-to-favorite', kwargs={'item_slug': self.slug})


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    Item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

# class Battery(models.Model):
#     but = models.CharField(max_length=100, db_index=True, verbose_name='Батарея')
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', null=True)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('but', kwargs={'but_slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        if self.item.discount:
            return self.quantity * (self.item.price - (self.item.price * (self.item.discount / 100)))
        else:
            return self.quantity * self.item.price

    # def get_total_order_price(self):
    #     return self.get_total_item_price()

    def get_final_price(self):

        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True)
    first_name = models.CharField(max_length=200,  blank=True, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    street_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    index = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    first_name_np = models.CharField(max_length=200, blank=True, null=True)
    last_name_np = models.CharField(max_length=200, null=True)
    phone_np = models.CharField(max_length=200, null=True)
    city_np = models.CharField(max_length=200, null=True)
    address_np = models.CharField(max_length=200, null=True)
    order_notes = models.TextField(max_length=5000, null=True, blank=True)



    def __str__(self):
        return self.user.user_name
    def ordered_item_list(self, slug):
        item_order = Order.objects.filter(user=self.user)
        if 'TK905' in 'TK905':
            return True

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class City(models.Model):
    ref = models.CharField(max_length=100)
    name = models.CharField(max_length=20)

    def __str__(self):
        return (str(self.name))


class Favorite(models.Model):
    item_favorite = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.item_favorite.slug


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    feedback_text = models.TextField(max_length=5000, null=True, blank=True)