from django import template
from ..models import Category, Item

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


@register.inclusion_tag('store/list_related.html')
def get_items():
    related = Item.objects.filter(id__lte = 4)
    return {'related': related}

