from django.shortcuts import render, redirect
from . models import Feedback
from store.models import Order, OrderItem, Item
from django.utils import timezone

def feedback_product(request):
    if request.method == 'POST':
        orders = OrderItem.objects.filter(user=request.user, ordered=True)
        for order in orders:
            if order.item.slug in request.POST['slug']:
                Feedback.objects.get_or_create(feedback_text=request.POST['feedback_text'],
                                               user_feedback=request.user.first_name,
                                               time_feedback=timezone.now(),
                                               slug=request.POST['slug']
                                            )
                break
    return redirect(request.META.get('HTTP_REFERER'))
# Create your views here.
