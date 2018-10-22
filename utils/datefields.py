from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

DATE_DEFAULTS = {
    'placeholder': _('yyyy-mm-dd'),
    'type': 'date',
}

TIME_DEFAULTS = {
    'placeholder': _('HH:MM'),
    'type': 'time',
}


class DateInput(forms.DateInput):
    def __init__(self, attrs={}):
        defaults = TIME_DEFAULTS.copy()
        defaults.update(attrs)
        super().__init__(attrs=defaults)


class TimeInput(forms.TimeInput):
    def __init__(self, attrs={}):
        defaults = DATE_DEFAULTS.copy()
        defaults.update(attrs)
        super().__init__(attrs=defaults)


class DateTimeInput(forms.SplitDateTimeWidget):
    def __init__(self, date_attrs={}, time_attrs={}):
        date_defaults = DATE_DEFAULTS.copy()
        date_defaults.update(date_attrs)

        time_defaults = TIME_DEFAULTS.copy()
        time_defaults.update(time_attrs)

        super().__init__(date_attrs=date_defaults, time_attrs=time_defaults)


class DateFormField(forms.DateField):
    widget = DateInput


class DateTimeFormField(forms.SplitDateTimeField):
    widget = DateTimeInput


class DateField(models.DateField):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', DateFormField)
        return super().formfield(**kwargs)


class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', DateTimeFormField)
        return super().formfield(**kwargs)
