from django.db import models
from django.urls import reverse
from selenium

LABEL_CHOICES = (
    ('Новика', 'Новинка'),
    ('Популярне', 'Популярне'),
)



class Item(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='Назва товару')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to='img', null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Ціна товару')
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Знижка у %')
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Опис')
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True, verbose_name='Акційна мітка')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True )


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('itemv', kwargs={'item_slug': self.slug})

    def discount_price_calculation(self):
        self.discount_price = self.price - (self.price * (self.discount/100))
        return self.discount_price

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    Item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    # def get_top_sales(self):
    #     self.top_sales = Item.objects.filter(label='Популярне')
    #     return self.top_sales



