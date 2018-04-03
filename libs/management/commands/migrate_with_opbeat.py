import logging

from django.core.management.commands.migrate import Command as Migrate

logger = logging.getLogger('opbeat')


class Command(Migrate):
    """Custom ``migrate`` management command

    If something goes wrong with migrations, notify into opbeat

    """

    def handle(self, *args, **options):
        try:
            return super().handle(*args, **options)
        except Exception as e:
            logger.error('There is something wrong with migrations',
                         exc_info=True)
            # Raise exception to have not 0 exit code
            raise e
