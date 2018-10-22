import pickle

from django.db import models


class PickleField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        # HACK: bypasse editable=False on BinaryField
        models.Field.__init__(self, *args, **kwargs)

    def deconstruct(self, *args, **kwargs):
        # HACK: bypasse editable=False on BinaryField
        return models.Field.deconstruct(self, *args, **kwargs)

    def get_prep_value(self, value):
        b = pickle.dumps(value)
        return super().get_prep_value(b)

    def from_db_value(self, b, expression, connection):
        return pickle.loads(b)

    def to_python(self, value):
        return value
