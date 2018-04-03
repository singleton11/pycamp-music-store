import datetime
from unittest.mock import patch

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils import timezone

from rest_framework.exceptions import ValidationError

import pytz

from ....api.serializers.fields import CustomLocationField, DateTimeFieldWithTZ


class CustomLocationFieldTestCase(TestCase):
    """Test case for ``CustomLocationField``"""

    def setUp(self):
        self.field = CustomLocationField()

        self.invalid_data = (
            ('Test', 'Should raise validation error when not dict passed'),
            ({}, 'Should raise validation error when empty dict passed'),
            ({'longitude': 12},
             'Should raise validation error when `latitude` is missing'),
            ({'latitude': 12},
             'Should raise validation error when `longitude` is missing'),
            ({'longitude': 190, 'latitude': 12},
             'Should raise validation error when `longitude` is not in range'),
            ({'longitude': -190, 'latitude': 12},
             'Should raise validation error when `longitude` is not in range'),
            ({'longitude': 12, 'latitude': 100},
             'Should raise validation error when `latitude` is not in range'),
            ({'longitude': 12, 'latitude': -100},
             'Should raise validation error when `latitude` is not in range')
        )

    def test_validation_on_invalid_data(self):
        """Test validation when data is invalid.

        Any data from ``invalid_data`` should raise ``ValidationError``. The
        second element of any tuple of ``invalid_data`` is message, which
        should outputs if exception which is not expected raises.
        """
        for data, message in self.invalid_data:
            message = '{message} {data}'.format(message=message, data=data)
            try:
                with self.assertRaises(ValidationError, msg=message):
                    self.field.to_internal_value(data)
            except Exception:
                self.fail(message)

    def test_dict_to_point_converting(self):
        """Test ``to_internal_value``"""
        location = {
            'longitude': 12,
            'latitude': 12
        }
        point = self.field.to_internal_value(location)
        self.assertEqual(point.coords,
                         (location['longitude'], location['latitude']))

    def test_point_to_dict_converting(self):
        """Test ``to_representation``"""
        point = Point(12, 12)
        location = self.field.to_representation(point)
        self.assertEqual((location['longitude'], location['latitude']),
                         point.coords)


class DateTimeFieldWithTZTestCase(TestCase):
    """Test case for ``DateTimeFieldWithTZ``"""

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
