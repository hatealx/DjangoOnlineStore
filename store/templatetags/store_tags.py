from django import template
from ..models import Product, Category
register = template.Library()

@register.inclusion_tag('appbar.html')
def get_categories():
    categories = Category.objects.all()
    return {'categories': categories}
