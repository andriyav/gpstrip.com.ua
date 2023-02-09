from django.urls import path
from .views import feedback_product


urlpatterns = [
    path('feedback-product/', feedback_product, name='feedback-product'),


]