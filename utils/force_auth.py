from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin


class ForceLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in settings.FORCE_LOGIN_IGNORE:
            return
        if not request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
            )
