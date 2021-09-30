from django import template

from apps.menu.models import Menu

register = template.Library()


@register.simple_tag
def headermenu(request):
    return Menu.objects.filter(pos='H')


@register.simple_tag
def footerermenu(request):
    return Menu.objects.filter(pos='F')
