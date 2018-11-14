from django.conf import settings
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import get_language


# inspired by https://github.com/perplexionist/django-translations/
class Translation(models.Model):
    language = models.CharField(max_length=32, choices=settings.LANGUAGES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=128)
    content_object = GenericForeignKey()
    field = models.CharField(max_length=64)
    text = models.TextField()

    class Meta:
        unique_together = ('language', 'content_type', 'object_id', 'field')


class TranslationInline(GenericTabularInline):
    model = Translation


def translate(instance, field, lang=None):
    if lang is None:
        lang = get_language()
    content_type = ContentType.objects.get_for_model(instance)
    try:
        return Translation.objects.get(
            content_type=content_type,
            object_id=instance.pk,
            field=field,
            language=lang)
    except Translation.DoesNotExist:
        return getattr(instance, field)


translate_lazy = lazy(translate, str)
