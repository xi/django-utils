from django.conf import settings
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import get_language


class Translation(models.Model):
    language = models.CharField(max_length=32, choices=settings.LANGUAGES)
    msgid = models.CharField(max_length=256)
    msgstr = models.CharField(max_length=256)

    class Meta:
        unique_together = ('language', 'msgid')


def translate(instance, field, lang=None):
    if lang is None:
        lang = get_language()
    msgid = getattr(instance, field)
    try:
        return Translation.objects.get(language=lang, msgid=msgid)
    except Translation.DoesNotExist:
        return msgid


translate_lazy = lazy(translate, str)
