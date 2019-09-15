from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin


class GetFormMixin(FormMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs


class GetFormView(GetFormMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        raise NotImplementedError
