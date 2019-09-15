from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest


def supports_readonly(field):
    input_type = getattr(field.widget, 'input_type', 'text')
    return not (
        hasattr(field, 'choices') or input_type in ['checkbox', 'radio', 'file']
    )


class ReadonlyFormMixin:
    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)

        if self.readonly:
            for field in self.fields.values():
                if supports_readonly(field):
                    field.widget.attrs['readonly'] = True
                else:
                    field.widget.attrs['disabled'] = True


class ReadonlyModelForm(ReadonlyFormMixin, forms.ModelForm):
    pass


class ReadonlyMixin:
    def get_readonly(self):
        raise NotImplementedError

    def get_form_class(self):
        if self.form_class:
            if issubclass(self.form_class, ReadonlyFormMixin):
                return self.form_class
            else:
                msg = 'form_class is not a subclass of ReadonlyFormMixin'
                raise ImproperlyConfigured(msg)
        return forms.modelform_factory(
            self.model, fields=self.fields, form=ReadonlyModelForm
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['readonly'] = self.get_readonly()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readonly'] = self.get_readonly()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.get_readonly():
            return HttpResponseBadRequest()
        return super().post(request, *args, **kwargs)
