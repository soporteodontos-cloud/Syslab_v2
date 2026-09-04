from django import template
from django.contrib.auth.models import Group

from core.utils import separador_de_miles, separador_de_miles_entero

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='separar')
def separar(value):
   return separador_de_miles(value)

@register.filter(name='separar_entero')
def separar_entero(value):
   return separador_de_miles_entero(value)

@register.filter(name='items')
def times(number):
    return range(number, 12)

@register.simple_tag(name='suma')
def add(a, b):
    return a+b

@register.filter(name='in_group')
def user_in_group(user, group_list):
    groups = Group.objects.filter(name__in=group_list.split(','))
    return bool(groups.filter(user=user).exists())