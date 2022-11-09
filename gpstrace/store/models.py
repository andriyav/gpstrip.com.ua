from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


LABEL_CHOICES = (
    ('Новинка', 'Новинка'),
    ('Популярне', 'Популярне'),
)
BATTERY_CHOICES = (
    ('1000 мАгод', '1000 мАгод'),
    ('5000 мАгод', '5000 мАгод'),
    ('10000 мАгод', '10000 мАгод'),
    ('20000 мАгод', '20000 мАгод'),

)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='Назва товару')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to='img', null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Ціна товару')
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Знижка у %')
    short_description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Короткий опис')
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Опис')
    details = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Деталі')
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True, verbose_name='Акційна мітка')
    battery = models.CharField(choices=BATTERY_CHOICES, max_length=20, null=True, blank=True,
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
            return self.quantity * self.item.price - (self.item.price * (self.item.discount / 100))
        else:
            return self.quantity * self.item.price

    def get_total_order_price(self):
        return self.get_total_item_price()

    def get_final_price(self):

        return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    street_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    index = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    item_favorite = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username