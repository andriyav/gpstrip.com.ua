from django.urls import path

from . views import *

# app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/<slug:item_slug>/', ShowItem.as_view(), name='itemv'),
    path('category/<slug:cat_slug>/', CategoryTracker.as_view(), name='category')
    ]