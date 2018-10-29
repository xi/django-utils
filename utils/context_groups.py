from django import template
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import mixins as auth_mixins

register = template.Library()


class Context(models.Model):
    pass


class ContextGroup(models.Model):
    name = models.CharField(max_length=80)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

    def get_permissions(self):
        perms = self.permissions.values_list(
            'content_type__app_label',
            'codename'
        )
        return ['{}.{}'.format(ct, name) for ct, name in perms]

    def has_perm(self, perm):
        return perm in self.get_permissions()


class BaseBackend:
    def authenticate(self, username, password):
        return None

    def get_group_permissions(self, user, obj=None):
        return set()

    def get_all_permissions(self, user, obj=None):
        return self.get_group_permissions(user, obj=obj)

    def has_perm(self, user, perm, obj=None):
        # you may want to override this for performance reasons
        perms = self.get_all_permissions(user, obj=obj)
        return perm in perms


class BasicObjectBackend(BaseBackend):
    # See https://code.djangoproject.com/ticket/20218

    def get_group_permissions(self, user, obj=None):
        if obj is None:
            return set()
        return user.get_group_permissions()

    def get_all_permissions(self, user, obj=None):
        if obj is None:
            return set()
        return user.get_all_permissions()

    def has_perm(self, user, perm, obj=None):
        if obj is None:
            return False
        return user.has_perm(perm)


class ContextPermissionBackend(BaseBackend):
    def get_group_permissions(self, user, obj=None):
        perms = set()
        if user.is_active and isinstance(obj, Context):
            groups = ContextGroup.objects.filter(context=obj, users=user)
            for group in groups:
                perms.update(group.get_permissions())
        return perms


class PermissionRequiredMixin(auth_mixins.PermissionRequiredMixin):
    def get_permission_object(self):
        return None

    def has_permission(self):
        perms = self.get_permission_required()
        permission_object = self.get_permission_object()
        return self.request.user.has_perms(perms, obj=permission_object)


@register.simple_tag
def has_perm(perm, user, obj=None):
    return user.has_perm(perm, obj)
