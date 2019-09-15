from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

DATE_FORMAT = '%Y-%m-%d'

DATE_DEFAULTS = {
    'placeholder': _('yyyy-mm-dd'),
    'type': 'date',
}

TIME_FORMAT = '%H:%M'

TIME_DEFAULTS = {
    'placeholder': _('HH:MM'),
    'type': 'time',
}


class DateInput(forms.DateInput):
    def __init__(self, attrs={}, **kwargs):
        defaults = DATE_DEFAULTS.copy()
        defaults.update(attrs)
        super().__init__(format=DATE_FORMAT, attrs=defaults, **kwargs)


class TimeInput(forms.TimeInput):
    def __init__(self, attrs={}, **kwargs):
        defaults = TIME_DEFAULTS.copy()
        defaults.update(attrs)
        super().__init__(format=TIME_FORMAT, attrs=defaults, **kwargs)


class DateTimeInput(forms.SplitDateTimeWidget):
    def __init__(self, date_attrs={}, time_attrs={}, **kwargs):
        date_defaults = DATE_DEFAULTS.copy()
        date_defaults.update(date_attrs)

        time_defaults = TIME_DEFAULTS.copy()
        time_defaults.update(time_attrs)

        super().__init__(
            date_format=DATE_FORMAT,
            date_attrs=date_defaults,
            time_format=TIME_FORMAT,
            time_attrs=time_defaults,
            **kwargs
        )


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
