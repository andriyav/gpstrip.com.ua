from django.urls import path

from . views import *




urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('item/<slug:item_slug>/', ShowItem.as_view(), name='itemv'),
    path('category/<slug:cat_slug>/', CategoryTracker.as_view(), name='category'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('index', HomeView.as_view(), name='index'),
    path('cart', CartView.as_view(), name='cart'),
    path('logout/', logout_user, name='logout'),
    path('add-to-favorite/<slug:item_slug>/', add_to_favorite, name='add-to-favorite'),
    path('remove-from-favorite/<slug:item_slug>/', remove_from_favorite, name='remove-from-favorite'),
    path('search', Search.as_view(), name='search'),
    path('about/', About.as_view(), name='about'),
    path('delivery/', delivery, name='delivery'),
    path('payment/', payment, name='payment'),
    path('return_terms/', return_terms, name='return_terms'),
    path('contacts/', contacts, name='contacts'),
    path('city-json/', get_json_car_data, name='city-json'),
    path('address-json/<str:city>/', get_json_address_data, name='address-json'),
    path('np_api/', np_api, name='np_api'),

    ]