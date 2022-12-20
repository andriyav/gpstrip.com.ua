import json
from json import JSONEncoder
import requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.core.mail import send_mail
from django.contrib.auth import logout, login

from .models import Item, Category, City, Order, Favorite
from .forms import CheckoutForms
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse


class HomeView(ListView):
    model = Item
    template_name = "store/items.html"
    context_object_name = 'items'

    def get_queryset(self):
        if '1000' in self.request.GET:
            return Item.objects.filter(battery='1000 мАгод')
        elif '5000' in self.request.GET:
            return Item.objects.filter(battery='5000 мАгод')
        elif '10000' in self.request.GET:
            return Item.objects.filter(battery='10000 мАгод')
        elif '20000' in self.request.GET:
            return Item.objects.filter(battery='20000 мАгод')

        else:
            if 'pricerange' in self.request.GET:
                price_range = self.request.GET['pricerange']
                f = price_range.split(',')
                price_min = float(f[0])
                price_max = float(f[1])
                return Item.objects.filter(price__lte=price_max, price__gte=price_min)
        if 'dropdown' in self.request.GET:
            filter = self.request.GET['dropdown']
        else:
            return Item.objects.all()
        if filter == 'popular':
            return Item.objects.order_by('-label')
        elif filter == 'price':
            return Item.objects.order_by('price')
        elif filter == 'discount':
            return Item.objects.order_by('-discount')

    def show_discount_30(self):
        return Item.objects.filter(discount='30')


class ShowItem(DetailView, JSONEncoder):
    model = Item
    template_name = 'store/product.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item_view'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['item_view']
        context['item_view'] = context['item_view']

        return context


class CategoryTracker(ListView):
    model = Item
    template_name = 'store/items.html'
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


class CartView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    redirect_field_name = 'cart'

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'store/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class CheckOutView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        form = CheckoutForms()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
        city = City.objects.all()
        context = {
            'form': form,
            'ob_item': order,
            'city': city
        }
        return render(self.request, "store/checkout.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForms(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                order.first_name = form.cleaned_data.get('first_name')
                order.last_name = form.cleaned_data.get('last_name')
                order.street_address = form.cleaned_data.get('street_address')
                order.city = form.cleaned_data.get('city')
                order.email = form.cleaned_data.get('email')
                order.index = form.cleaned_data.get('index')
                order.phone = form.cleaned_data.get('phone')
                order.first_name_np = form.cleaned_data.get('first_name_np')
                order.last_name_np = form.cleaned_data.get('last_name_np')
                order.phone_np = form.cleaned_data.get('phone_np')
                order.city_np = request.POST.get('city-np')
                order.address_np = request.POST.get('address-np')
                order.ordered_date = timezone.now()
                order.save()
                order.ordered = True
                order.save()
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                send_mail(
                    'Замовлення',
                    f'Ви отримали замовлення від {order.first_name_np}/n {order.city_np}',
                    'andriyav@hotmail.com',
                    ['andriyav@hotmail.com'],
                    fail_silently=False,
                )
                return redirect('checkout')
            messages.warning(self.request, 'Помилка форми')
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('checkout')


class IndexView(ListView):
    model = Item
    template_name = "store/index.html"
    context_object_name = 'index_items'


class About(ListView):
    model = Item
    template_name = "store/about.html"


def logout_user(request):
    logout(request)
    return redirect('home')


class Search(ListView):
    model = Item
    template_name = 'store/search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        return Item.objects.filter(description__icontains=self.request.GET.get('q', ''))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


@login_required
def add_to_favorite(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    item_favorite, created = Favorite.objects.get_or_create(
        item_favorite=item,
        user=request.user,
    )
    item_favorite.save()
    messages.info(request, "Товар добавлено в улюблене")
    return redirect("index")


@login_required
def remove_from_favorite(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    item_favorite = Favorite.objects.filter(
        item_favorite=item,
        user=request.user,
    )
    item_favorite.delete()
    messages.info(request, "Товар було видалено з улюблених")
    return redirect("index")


def get_json_car_data(request):
    qs_val = list(City.objects.values())
    return JsonResponse({'data': qs_val})


def get_json_address_data(request, *args, **kwargs):
    selected_city = kwargs.get('city')
    obj_address_list = []
    ref = City.objects.get(name=selected_city).ref
    param = {
        "apiKey": "0139a34f622b2f7ac7cd63936a5f4150",
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": ref
        }}
    url = 'https://api.novaposhta.ua/v2.0/json/'
    np = requests.post(url, json.dumps(param))
    for city in np.json()['data']:
        obj_address_list.append(city['Description'])
    return JsonResponse({'data': obj_address_list})

def np_api(request):
    params = '''{
    	"apiKey": "0139a34f622b2f7ac7cd63936a5f4150",
    	"modelName": "Address",
    	"calledMethod": "getCities",
    	"methodProperties": {
    		"FindByString": ""
    	}
    }'''
    url = 'https://api.novaposhta.ua/v2.0/json/'
    np = requests.post(url, params)
    for city in np.json()['data']:
        print(city['Description'])
        order_item, created = City.objects.get_or_create(name=city['Description'], ref=city['Ref'])
    return redirect("index")

def delivery(request):
    return render(request, "store/delivery.html")


def payment(request):
    return render(request, "store/payment.html")


def return_terms(request):
    return render(request, "store/return_terms.html")


def contacts(request):
    return render(request, "store/contacts.html")
