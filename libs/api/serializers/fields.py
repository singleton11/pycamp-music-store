from collections import OrderedDict

from django.contrib.gis.geos import Point
from django.utils import timezone

from rest_framework import serializers


class DateTimeFieldWithTZ(serializers.DateTimeField):

    def enforce_timezone(self, value):
        """
        If `self.default_timezone` is `None`, always return naive datetimes.
        If `self.default_timezone` is not `None`, return aware datetimes.
        """
        try:
            tz = timezone._active.value
            if (self.default_timezone is not None) \
                    and not timezone.is_aware(value):
                return timezone.make_aware(value, tz)
            return value
        except AttributeError:
            return super().enforce_timezone(value)

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super().to_representation(value)


class CustomLocationField(serializers.Serializer):
    """Location field for representing points with 2 coordinates.

    django.contrib.gis.geos.Point represented using dict:
    {
        "longitude": 12,
        "latitude": 12
    }
    """

    longitude = serializers.FloatField(
        max_value=180,
        min_value=-180,
        required=True
    )
    latitude = serializers.FloatField(
        max_value=90,
        min_value=-90,
        required=True
    )

    def to_internal_value(self, value: dict) -> Point:
        """Convert ``dict`` to ``Point``

        Args:
            value (dict): Value to convert

        Returns:
            Point: Point with ``x=value['longitude']`` and
                ``y=value['latitude']``

        Raises:
            ValidationError: when value is not dict and latitude and longitude
                values not in according ranges
        """
        value = super().to_internal_value(value)
        return Point(value['longitude'], value['latitude'])

    def to_representation(self, obj: Point) -> OrderedDict:
        """Convert from ``Point`` to ``OrderedDict``.

        Args:
            obj (Point): Point to represent

        Returns:
            OrderedDict: Ordered dict with ``longitude`` and ``latitude`` keys
                and float values
        """
        return OrderedDict([
            ('longitude', obj.x),
            ('latitude', obj.y),
        ])
