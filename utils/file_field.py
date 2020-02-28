from django import forms
from django.utils.translation import gettext_lazy as _

import magic


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', [])
        self.max_upload_size = kwargs.pop('max_upload_size', 0)
        super().__init__(*args, **kwargs)

    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        if f.size > self.max_upload_size:
            raise forms.ValidationError(_('File is too big.'), code='size')

        content_type = magic.detect_from_content(f.read(1024)).mime_type
        if content_type not in self.content_types:
            raise forms.ValidationError(
                _('Filetype not supported.'), code='content_type'
            )
        f.seek(0)

        return f

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if self.content_types:
            attrs.setdefault('accept', ','.join(self.content_types))
        return attrs
