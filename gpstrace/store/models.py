from django.db import models
LABEL_CHOICES = (
    ('Новика', 'Новинка'),
    ('Популярне', 'Популярне'),
)



class Item(models.Model):
    title = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True )


    def __str__(self):
        return self.title

    def discount_price_calculation(self):
        self.discount_price = self.price - (self.price * (self.discount/100))
        return self.discount_price


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


    # def get_top_sales(self):
    #     self.top_sales = Item.objects.filter(label='Популярне')
    #     return self.top_sales



