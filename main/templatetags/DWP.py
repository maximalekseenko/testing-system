# setup
from django import template
register = template.Library()
# imports
from json import dumps
from datetime import datetime

@register.filter
def tojson(value):
    return dumps(value)

@register.filter
def tolist(value):
    return list(value)

@register.filter
def inpast(value, form):
    return datetime.now()>datetime.strptime(value,form)