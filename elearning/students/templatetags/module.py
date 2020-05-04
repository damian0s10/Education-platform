from django import template


register = template.Library()

@register.filter(name='check_style')
def check_style(modules, user):
    modules = modules.filter(learning_style = user.profile.learning_style)
    return modules