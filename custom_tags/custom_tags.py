from django import template

register = template.Library()

@register.simple_tag
def lesszero(a):
    return int(a * 1000)

@register.simple_tag
def worth(a, b, c):
    return round((a / b * c), 2)
