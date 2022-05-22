from django.shortcuts import render
from django.views.generic import ListView

from .models import Item


class HomeView(ListView):
    model = Item
    template_name = "store/store.html"
    #
    # def get_queryset(self):
    #     return Item.objects.filter(id=1)






