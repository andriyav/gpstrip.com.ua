from django import template
from ..models import Category, Item

register = template.Library()

@register.simple_tag()
def get_labeled(filter='Популярне'):
    if not filter:
        return Item.objects.all()
    else:
        return Item.objects.filter(label=filter)


@register.inclusion_tag('store/list_categories.html')
def get_categories():
    cats = Category.objects.all()
    return {'cats': cats}


@register.inclusion_tag('store/list_related.html')
def get_items():
    related = Item.objects.filter(id__lte = 4)
    return {'related': related}

