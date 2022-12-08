from django.urls import path

from . views import *




urlpatterns = [
    path('', IndexView.as_view(), name='home'),
        path('item/<slug:item_slug>/', ShowItem.as_view(), name='itemv'),
    path('category/<slug:cat_slug>/', CategoryTracker.as_view(), name='category'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('index', HomeView.as_view(), name='index'),
    path('cart', CartView.as_view(), name='cart'),
    # path('register', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    # path('login/', LoginUser.as_view(), name='login'),
    # path('add-to-cart/<slug:item_slug>/', add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('add-to-favorite/<slug:item_slug>/', add_to_favorite, name='add-to-favorite'),
    path('remove-from-favorite/<slug:item_slug>/', remove_from_favorite, name='remove-from-favorite'),
    path('search', Search.as_view(), name='search'),

    ]