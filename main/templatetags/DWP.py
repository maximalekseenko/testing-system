from django import template
register = template.Library()
from json import dumps

@register.filter
def tojson(value):
    return dumps(value)

