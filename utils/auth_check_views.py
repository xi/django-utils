"""
This is a draft implementation.

-   It only checks class based views.
-   There can be many ways to check for login. This only checks that a
    view inherits from LoginRequiredMixin or PermissionRequiredMixin.

"""

import re

from django.core.checks import Error, register

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

IGNORE = [
    re.compile('^/login/$'),
    re.compile('^/logout/$'),
    re.compile('^/media/'),
    re.compile('^/admin/'),
    re.compile('^/__debug__/'),
    re.compile('^/jsi18n/'),
]


def iter_views(resolver=None, path=''):
    if resolver is None:
        from django.urls import get_resolver
        resolver = get_resolver()
    path += str(resolver.pattern).lstrip('^')
    if getattr(resolver, 'callback', None):
        yield resolver.callback, path
    for child in getattr(resolver, 'url_patterns', []):
        for c, p in iter_views(child, path):
            yield c, p


@register()
def check_permission_required(app_configs, **kwargs):
    errors = []
    for view, path in iter_views():
        if not hasattr(view, 'view_class'):
            continue
        if (
            hasattr(view.view_class, 'permission_required')
            and not issubclass(view.view_class, PermissionRequiredMixin)
        ):
            errors.append(Error(
                'The class-based-view {!r} at {} has an attribute called '
                '``permission_required``, but does not inherit from '
                'PermissionRequiredMixin'.format(view.view_class, path),
                obj=view.view_class,
                id='auth.E001',
            ))
    return errors


@register()
def check_login(app_configs, **kwargs):
    errors = []
    for view, path in iter_views():
        if not hasattr(view, 'view_class'):
            continue
        if any(p.search(path) for p in IGNORE):
            continue
        if (
            not issubclass(view.view_class, PermissionRequiredMixin)
            and not issubclass(view.view_class, LoginRequiredMixin)
        ):
            errors.append(Error(
                'The class-based-view {!r} at {} does not inherit from '
                'LoginRequiredMixin or '
                'PermissionRequiredMixin'.format(view.view_class, path),
                hint='You can add a pattern to IGNORE',
                obj=view.view_class,
                id='auth.E002',
            ))
    return errors
