# setup
from django import template
from django.utils import timezone
register = template.Library()
# imports
from json import dumps
from datetime import datetime
from pytz import UTC

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