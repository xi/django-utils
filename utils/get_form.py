from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin


class GetFormMixin(FormMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class GetFormView(GetFormMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
