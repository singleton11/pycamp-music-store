from unittest.mock import MagicMock

from django.test import TestCase

from libs.middleware import TimezoneMiddleware


class TimezoneMiddlewareTestCase(TestCase):
    """Test case for ``TimezoneMiddleware``"""

    def setUp(self):
        self.middleware = TimezoneMiddleware()
        self.request = MagicMock()

    def test_process_request(self):
        """Ensure that is ``tzname`` not in ``pytz`` available timezones
        have no side effects
        """
        self.request.META = {'HTTP_USER_TIMEZONE': 'Test'}
        self.middleware.process_request(self.request)
        self.assertIsInstance(self.request, MagicMock)

    def test_if_tzname_is_none(self):
        """Ensure, that if header is not exists, function call have no side
        effects
        """
        self.request.META = {}
        self.middleware.process_request(self.request)
        self.assertIsInstance(self.request, MagicMock)

    def test_if_tzname_is_correct(self):
        """Ensure, that if correct timezone passed in headers
        ``request.timezone`` will store timezone
        """
        timezone = 'Asia/Krasnoyarsk'
        self.request.META = {'HTTP_USER_TIMEZONE': timezone}
        self.middleware.process_request(self.request)
        # Assert side effects
        self.assertEqual(str(self.request.timezone), timezone)
