from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item, Category


class HomeView(ListView):
    model = Item
    template_name = "store/store.html"
    context_object_name = 'items'

    def get_queryset(self):
        if 'dropdown' in self.request.GET:
            filter = self.request.GET['dropdown']
        else:
            filter = False
        if filter == 'popular':
            return Item.objects.order_by('-label')
        if filter == 'price':
            return Item.objects.order_by('price')
        if filter == 'discount':
            return Item.objects.order_by('-discount')
        else:
            return Item.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'max' in self.request.GET and 'min' in self.request.GET:
            price_max = self.request.GET['max']
            price_min = self.request.GET['min']
            price_filter = Item.objects.filter(price__lte=price_max, price__gte=price_min)
        else:
            price_filter = Item.objects.all()
        context['title'] = 'Інтернет магазин GPSTrace'
        context['items'] = price_filter

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


class CategoryTracker(ListView):
    model = Item
    template_name = 'store/store.html'
    context_object_name = 'items'
    allow_empty = False

    def get_queryset(self):
        return Item.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категорія -' + str(context['items'][0].cat)
        return context


class ShowCategory(ListView):
    model = Category
    template_name = 'store/store.html'
    context_object_name = 'cats'

class BlankView(ListView):
    model = Item
    template_name = "store/blank.html"
    context_object_name = 'blank'