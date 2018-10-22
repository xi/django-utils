from django.utils.http import is_safe_url


class NextMixin:
    redirect_field_name = 'next'

    def get_success_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name))
        if not redirect_to:
            if self.success_url is not None:
                redirect_to = self.success_url
            elif self.object:
                redirect_to = self.object.get_absolute_url()
        host = self.request.get_host()
        if redirect_to and is_safe_url(redirect_to, allowed_hosts={host}):
            return redirect_to
        else:
            return ''
