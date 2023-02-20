import json
from json import JSONEncoder
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout
from .models import Item, Category, City, Order, Favorite
from .forms import CheckoutForms
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class HomeView(ListView):
    model = Item
    template_name = "store/store.html"
    context_object_name = 'items'

    def get_queryset(self):
        if 'pricerange' in self.request.GET:
            price_range = self.request.GET['pricerange']
            f = price_range.split(',')
            price_min = float(f[0])
            price_max = float(f[1])
            return Item.objects.filter(price__lte=price_max, price__gte=price_min)
        if 'dropdown' in self.request.GET:
            filter = self.request.GET['dropdown']
            if filter == 'popular':
                return Item.objects.order_by('-label').select_related('cat')
            if filter == 'price':
                return Item.objects.order_by('price').select_related('cat')
            if filter == 'discount':
                return Item.objects.order_by('-discount').select_related('cat')

        battery_range = []
        for i in self.request.GET:
            battery_range.append(int(i))
        if battery_range == []:
            return Item.objects.all().select_related('cat')
        else:
            if len(battery_range) == 1:
                print(battery_range[0])
                return Item.objects.filter(battery=battery_range[0]).select_related('cat')
            if len(battery_range) == 2:
                print(battery_range[1])
                return Item.objects.filter(Q(battery=battery_range[0]) | Q(battery=battery_range[1])).select_related('cat')
            if len(battery_range) == 3:
                return Item.objects.filter(
                    Q(battery=battery_range[0]) | Q(battery=battery_range[1]) | Q(battery=battery_range[2])).select_related('cat')
            if len(battery_range) == 4:
                return Item.objects.filter(
                    Q(battery=battery_range[0]) | Q(battery=battery_range[1]) | Q(battery=battery_range[2]) | Q(
                        battery=battery_range[3])).select_related('cat')


    def show_discount_30(self):
        return Item.objects.filter(discount='30').select_related('cat')


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

class ShowFavorite(ListView):
    model = Favorite
    template_name = 'store/favorite.html'
    context_object_name = 'favorite'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            favorite_item = Favorite.objects.filter(user=self.request.user)
            return favorite_item

class CategoryTracker(ListView):
    model = Item
    template_name = 'store/store.html'
    context_object_name = 'items'
    allow_empty = False

    def get_queryset(self):
        return Item.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

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
            messages.warning(self.request, "У Вас не має активних замовлень")
            return redirect("/")


class CheckOutView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        form = CheckoutForms()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.warning(self.request, "У вас не має активних замовлень")
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
                try:
                    city_np_class = City.objects.get(ref=request.POST.get('city-np'))
                    order.city_np = city_np_class.name
                    order.address_np = request.POST.get('address-np')
                except:
                    order.city_np = form.cleaned_data.get('city_np')
                    order.address_np = form.cleaned_data.get('address_np')
                order.order_notes = form.cleaned_data.get('order_notes')
                order.ordered_date = timezone.now()
                order.total = order.get_total()
                # subject, from_email, to, cc = 'Замовлення GPSTrace', 'andriyav@gpstrip.com.ua', request.user.email, 'andriyav@hotmail.com'
                # text_content = 'This is an important message.'
                # html_content = render_to_string('store/order_letter.html', {'ob_item': order})
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [cc])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                subject, from_email, to, cc = 'Замовлення GPSTrace', 'andriyav@hotmail.com', request.user.email, 'andriyav@hotmail.com'
                text_content = 'This is an important message.'
                html_content = render_to_string('store/order_letter.html', {'ob_item': order})
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [cc])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                order.ordered = True
                order.save()
                return redirect('checkout')
            messages.warning(self.request, 'Помилка форми')
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "У Вас не має активних замовлень")
            return redirect('checkout')


class IndexView(ListView):
    model = Item
    template_name = "store/index.html"
    context_object_name = 'index_items'

    def get_queryset(self):
        return Item.objects.all().select_related('cat')


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

        return Item.objects.filter(Q(description__icontains=self.request.GET.get('drop', '')) &
                                   Q(description__icontains=self.request.GET.get('q', '')))

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
    messages.success(request, "Товар добавлено в улюблене")

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_favorite(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    item_favorite = Favorite.objects.filter(
        item_favorite=item,
        user=request.user,
    )
    item_favorite.delete()
    messages.info(request, "Товар було видалено з улюблених")
    return redirect(request.META.get('HTTP_REFERER'))


def get_json_car_data(request):                                # Функція формування переліку
    qs_val = list(City.objects.values())
    return JsonResponse({'data': qs_val})


def get_json_address_data(request, *args, **kwargs):            # Функція завантаження вулиць нової пошти заданого міста
    selected_city = kwargs.get('city') # надання змінній назви міста з url address-json/<str:city>/
    obj_address_list = []                                       # ініціалізація преліку адресів міста
    ref = kwargs.get('city')
    print(ref, 'ref', kwargs.get)# ref номеру міста із бази даних.
    param = {
        "apiKey": "0139a34f622b2f7ac7cd63936a5f4150",
        "modelName": "Address",
        "calledMethod": "getWarehouses",                         # формування даних для пердачі на API нової пошти. Форма взята з сайта нової пошти
        "methodProperties": {
            "CityRef": ref
        }}
    url = 'https://api.novaposhta.ua/v2.0/json/'                 # url для відправки форми API
    np = requests.post(url, json.dumps(param))                   # відправка форми API в json форматі
    for city in np.json()['data']:                               # отримання response за ключем 'data' переліку вулиць
        obj_address_list.append(city['Description'])             # формування листу вулиць
    return JsonResponse({'data': obj_address_list})              # повернення переліку вулиць


def np_api(request):                                             # форма для передачі для пердачі на API нової пошти для отримання переліку міст нвової пошти. Форма взята з сайта нової пошти
    params = '''{                                                
    	"apiKey": "0139a34f622b2f7ac7cd63936a5f4150",            
    	"modelName": "Address",                                  
    	"calledMethod": "getCities",
    	"methodProperties": { 
    		"FindByString": ""
    	}
    }'''
    url = 'https://api.novaposhta.ua/v2.0/json/'                 # url для відправки форми API
    np = requests.post(url, params)                              # відправка форми API в json форматі
    for city in np.json()['data']:                               # отримання response за ключем 'data' переліку вулиць
        order_item, created = City.objects.get_or_create(
            name=city['Description'], ref=city['Ref']
        )                                                        # заповнення таблиці ази даних містами
    return redirect("index")                                     # переадресація на сторінку крамниці


def delivery(request):
    return render(request, "store/delivery.html")


def payment(request):
    return render(request, "store/payment.html")


def return_terms(request):
    return render(request, "store/return_terms.html")


def contacts(request):
    return render(request, "store/contacts.html")

#  np _api_list можна видалити
def np_api_list(request):                                             # форма для передачі для пердачі на API нової пошти для отримання переліку міст нвової пошти. Форма взята з сайта нової пошти
    params = '''{                                                
    	"apiKey": "0139a34f622b2f7ac7cd63936a5f4150",            
    	"modelName": "Address",                                  
    	"calledMethod": "getCities",
    	"methodProperties": { 
    		"FindByString": ""
    	}
    }'''
    url = 'https://api.novaposhta.ua/v2.0/json/'                 # url для відправки форми API
    np = requests.post(url, params)                              # відправка форми API в json форматі
    print(np.json()['data'])

    city_list = []
    city_ref = []
    for city in np.json()['data']:  # отримання response за ключем 'data' переліку вулиць
        city_list.append(city['Description'])
        city_ref.append(city['Ref'])
    return JsonResponse({'data': city_list, 'data_ref': city_ref})                                     # переадресація на сторінку крамниці