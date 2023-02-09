
from django.shortcuts import render, redirect
from . models import Feedback
def feedback_product(request):
    if request.method == 'POST':
        print(request.POST)
        Feedback.objects.get_or_create(feedback_text=request.POST['feedback_text'])
    return redirect(request.META.get('HTTP_REFERER'))
# Create your views here.
