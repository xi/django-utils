from django.apps import apps
from django.conf import settings


class AppDBRouter:
    """Route specific apps to specific databases.

    This router makes no statements about other apps, i.e. there is no
    guarantee that an app has exclusive access to a database. While
    database access is routed to 'default' by default, migrations are
    executed on all databases.

    Example configuration::

        APP_DB_ROUTER = {
            'some.app': 'database1',
            'other.app': 'database2',
        }
    """

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        return settings.APP_DB_ROUTER.get(app_label)

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        _db = settings.APP_DB_ROUTER.get(app_label)
        if _db is not None:
            return db == _db


class ModelDBRouter:
    def db_for_read(self, model, **hints):
        model_label = model._meta.label
        return settings.MODEL_DB_ROUTER.get(model_label)

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name:
            model = apps.get_model(app_label, model_name)
            _db = self.db_for_write(model)
            if _db:
                return db == _db
            elif db in settings.MODEL_DB_ROUTER.values():
                return False
