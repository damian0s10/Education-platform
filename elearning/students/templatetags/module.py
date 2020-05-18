from django import template
from django.db.models import Q

register = template.Library()

@register.filter(name='check_style')
def check_style(modules, user):
    modules = modules.filter(Q(learning_style = user.profile.learning_style) | Q(learning_style = 'wszyscy'))
    return modules 