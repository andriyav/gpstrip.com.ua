from django import template
from ..models import Category

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('store/list_categories.html')
def get_categories():
    cats = Category.objects.all()
    return {'cats': cats}



