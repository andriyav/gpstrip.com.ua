from django.contrib import admin

from .models import *

# admin.site.register(Item)
admin.site.register(Category)


class GalleryInline(admin.TabularInline):

    model = Gallery


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,]