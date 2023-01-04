from django.shortcuts import render
from . forms import SubscribersForm
# Create your views here.

def newsletter(request):
    form = SubscribersForm()
    contest = {
        'form': form,
    }
    return render(request, 'store/footer.html', contest)
