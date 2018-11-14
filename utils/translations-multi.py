from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import lazy
from django.utils.translation import get_language


def translate(instance, field, lang=None):
    if lang is None:
        lang = get_language()
    try:
        translation = instance.translation_set.get(language=lang)
        value = getattr(translation, field)
    except ObjectDoesNotExist:
        value = None
    if value:
        return value
    return getattr(instance, field)


translate_lazy = lazy(translate, str)
