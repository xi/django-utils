from functools import partialmethod

from django.db import models

from .implementation import translate_lazy


class TranslatableMixin:
    class TranslatableMeta:
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.TranslatableMeta.fields:
            name = 'get_{}_display'.format(field)
            setattr(self, name, lambda: translate_lazy(self, field))


class TranslatableField(models.StringField):
    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=private_only)

        fn = 'get_{}_display'.format(self.name)
        setattr(cls, fn, partialmethod(translate_lazy, self.name))
