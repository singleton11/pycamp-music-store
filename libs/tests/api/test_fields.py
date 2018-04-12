import datetime
from unittest.mock import patch
from unittest import skip

from django.test import TestCase
from django.utils import timezone

import pytz

from ...api.serializers.fields import DateTimeFieldWithTZ


class DateTimeFieldWithTZTestCase(TestCase):
    """Test case for ``DateTimeFieldWithTZ``"""

    @skip("Need fix")  # test fails randomly
    @patch('rest_framework.serializers.DateTimeField.enforce_timezone')
    def test_enforce_timezone(self, enforce_timezone):
        """Test ``enforce_timezone``"""
        date_field = DateTimeFieldWithTZ()
        current_datetime = datetime.datetime.now()
        date_field.enforce_timezone(current_datetime)
        enforce_timezone.assert_called_with(current_datetime)

    @patch('django.utils.timezone.make_aware')
    def test_enforce_timezone_timezone_active(self, make_aware):
        """Test ``enforce_timezone`` when timezone is activated, should call
        ``make_aware``"""
        timezone.activate(pytz.timezone('Asia/Krasnoyarsk'))
        date_field = DateTimeFieldWithTZ(
            default_timezone=pytz.timezone('Asia/Krasnoyarsk')
        )
        date_field.enforce_timezone(datetime.datetime.now())
        self.assertTrue(make_aware.called)

    def test_enforce_timezone_active_default_timezone_is_not_set(self):
        """Test ``enforce_timezone`` when timezone is activated, but
        ``default_timezone`` attribute of field is not set; timezone awared,
        should just return value"""
        timezone.activate(pytz.timezone('Asia/Krasnoyarsk'))
        date_field = DateTimeFieldWithTZ()
        current_datetime = timezone.make_aware(datetime.datetime.now())
        self.assertEqual(
            current_datetime,
            date_field.enforce_timezone(current_datetime)
        )

    @patch('rest_framework.serializers.DateTimeField.to_representation')
    def test_to_representation(self, to_representation):
        """Test ``to_representation``, before call this ``super`` method,
        should transform datetime to datetime with local timezone"""
        date_field = DateTimeFieldWithTZ()
        current_datetime = timezone.now()
        date_field.to_representation(current_datetime)
        to_representation.assert_called_with(
            timezone.localtime(current_datetime)
        )
