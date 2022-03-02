# setup
from django import template
from django.utils import timezone
register = template.Library()
# imports
from random import shuffle
from json import dumps
from pytz import UTC



@register.filter
def index(indexable, i):
    return indexable[i]



@register.filter
def tojson(value):
    return dumps(value)



@register.filter
def tolist(value):
    return list(value)



@register.filter
def inpast(value):
    return value < timezone.now() 



@register.filter
def filterlist(value, condition):
    return list(filter(lambda x: eval(condition), value))



@register.filter
def maplist(value, condition):
    return list(map(lambda x: eval(condition), value))



@register.filter
def shufflelist(value, on=True):
    if not on: return value 
    value = list(value)
    shuffle(value)
    return value