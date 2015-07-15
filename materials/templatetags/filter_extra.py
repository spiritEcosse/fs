__author__ = 'igor'
from django import template

register = template.Library()


def sub(value, arg):
    return value - arg


def percent(value, arg):
    if arg and value:
        return int(value * 100 / arg)
    return 0


@register.filter
def to_class_name(value):
    return value.__class__.__name__

register.filter('percent', percent)
register.filter('sub', sub)