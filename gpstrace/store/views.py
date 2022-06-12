from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item, Category


class HomeView(ListView):
    model = Item
    template_name = "store/store.html"
    context_object_name = 'items'

    # @staticmethod
    # def pageobjects(request):
    #     return request.GET['dropdown']

    def get_queryset(self):
        filter = self.request.GET['dropdown']
        if filter != 'popular':
            return Item.objects.all()
        else:
            return Item.objects.filter(label=filter)

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
