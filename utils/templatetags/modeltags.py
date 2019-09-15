from django import template
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    value = getter() if getter else getattr(instance, field_name)
    if value is True:
        return _('Yes')
    elif value is False:
        return _('No')
    elif value is None or value == '':
        return '—'
    elif hasattr(value, 'all'):
        return ', '.join(str(x) for x in value.all())


@register.filter(name='fields')
def fields(instance):
    return instance._meta.get_fields()
