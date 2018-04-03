from unittest.mock import patch

from django.core.management import call_command
from django.core.management.commands.migrate import Command
from django.test import TestCase


class TestMigrateWithOpbeat(TestCase):
    """Test case for ``migrate_with_opbeat`` management command"""

    @patch.object(Command, 'execute')
    @patch('logging.Logger.error')
    def test_migrate(self, error, handle):
        """Test ``migrate_with_opbeat`` without exceptions

        Ensure that ``error`` isn't executed when no exception raised when
        ``migrate_with_opbeat``

        """
        call_command('migrate_with_opbeat')
        self.assertEqual(error.call_count, 0)

    @patch.object(Command, 'handle', side_effect=Exception)
    @patch('logging.Logger.error')
    def test_migrate_with_exception(self, error, _):
        """Test ``migrate_with_opbeat`` with exception

        Ensure that ``logger.error`` will be executed if ``Exception`` raised
        when ``migrate_with_opbeat``

        """
        with self.assertRaises(Exception):
            call_command('migrate_with_opbeat')
            error.assert_called_with(
                'There is something wrong with migrations',
                exc_info=True
            )
