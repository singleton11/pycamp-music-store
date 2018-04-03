from django.utils import timezone

from rest_framework import serializers

__all__ = (
    'UploadSerializer',
    'LocationSerializer',
)


class UploadSerializer(serializers.Serializer):
    upload = serializers.ImageField(required=True)


class LocationSerializer(serializers.Serializer):
    """Location serializer.

    For use with GeoDjango model.

    """
    lat = serializers.DecimalField(max_digits=10, decimal_places=6,
                                   required=True)
    lon = serializers.DecimalField(max_digits=10, decimal_places=6,
                                   required=True)

    def to_representation(self, obj):
        lon, lat = obj.coords
        return {
            'lon': lon,
            'lat': lat
        }

    def to_internal_value(self, data):
        try:
            self.lon = data['lon']
            self.lat = data['lat']
            return 'POINT({0} {1})'.format(data['lon'], data['lat'])
        except KeyError:
            return super().to_internal_value(data)

    def save(self, user=None):
        if user:
            user.location = self.validated_data
            user.location_updated = timezone.now()
            user.save()
        return user
