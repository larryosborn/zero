from django.conf import settings
from django import template
register = template.Library()



@register.filter(name='number_class')
def number_class(num):
    if num > 0:
        return 'pos'
    elif num < 0:
        return 'neg'
    else:
        return 'neu'

