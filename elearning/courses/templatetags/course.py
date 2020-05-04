from django import template
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from ..models import Course

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='in_course')
def in_course(user, slug):
    course = get_object_or_404(Course, slug=slug)
    return True if user in course.students.all() else False

@register.filter(name='has_learning_style')
def has_learning_style(user):
    return True if user.profile.learning_style else False