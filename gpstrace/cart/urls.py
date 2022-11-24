from django.urls import path, include

from cart import views
from cart.views import add_to_cart, remove_from_cart
#
# app_name = 'cart'

urlpatterns = [
    path('cart2/', views.cart_summary, name='cart_summary'),
    path('add-to-cart/<slug:item_slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:item_slug>/', remove_from_cart, name='remove-from-cart'),
]