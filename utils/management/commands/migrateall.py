from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.commands.migrate import Command as MigrateCommand


class Command(BaseCommand):
    help = 'Update database schema of all databases.'

    def handle(self, *args, **kwargs):
        migrate = MigrateCommand()

        options = {
            'app_label': None,
            'migration_name': None,
            'interactive': True,
            'fake': False,
            'fake_initial': False,
            'run_syncdb': False,
        }
        options.update(kwargs)

        for database in settings.DATABASES:
            options['database'] = database
            if options['verbosity'] >= 1:
                self.stdout.write(self.style.MIGRATE_HEADING('Database:'))
                self.stdout.write('  ' + database)
            migrate.handle(*args, **options)
            if options['verbosity'] >= 1:
                self.stdout.write('')
