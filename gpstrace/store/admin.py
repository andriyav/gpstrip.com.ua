from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Favorite)

class GalleryInline(admin.TabularInline):

    model = Gallery


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,]