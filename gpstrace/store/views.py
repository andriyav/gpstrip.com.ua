from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item


class HomeView(ListView):
    model = Item
    template_name = "store/store.html"
    context_object_name = 'items'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Інтернет магазин GPSTrace'
        return context

class ShowItem(DetailView):
    model = Item
    template_name = 'store/product.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item_view'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['item_view']
        return context






