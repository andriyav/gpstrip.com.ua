from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('store/list_categories.html')
def get_categories():
    cats = Category.objects.all()
    return {'cats': cats}


