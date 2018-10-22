from django import template
from django.db import models

register = template.Library()


@register.filter(name='verbose_name')
def verbose_name(instance, field_name):
    field = instance._meta.get_field(field_name)
    if isinstance(field, models.Field):
        return field.verbose_name
    else:
        # FIXME: backrefs do not have a verbose_name
        return field.name


@register.filter(name='display')
def display(instance, field_name):
    getter = getattr(instance, 'get_{}_display'.format(field_name), None)
    if getter:
        return getter()
    else:
        return getattr(instance, field_name)


@register.filter(name='fields')
def fields(instance):
    return instance._meta.get_fields()
