from django import template
from datetime import datetime
import random

register = template.Library()

# filter for getting value of key in dict
@register.filter(name='getIdStr')
def getIdStr(obj, attribute):
    return obj[attribute]


@register.filter(name="randomItem")
def randomItem(obj):
    return random.choice(obj)


