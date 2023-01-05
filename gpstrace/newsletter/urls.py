from django.urls import path
from .views import newsletter_subscriber, message_send


#
# app_name = 'cart'

urlpatterns = [
    path('news-letter/', newsletter_subscriber, name='news-letter'),
    path('massage-send/', message_send, name='massage-send')

]