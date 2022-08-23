from django.contrib import admin

from .models import *

admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ShippingAddress)

class GalleryInline(admin.TabularInline):

    model = Gallery


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,]