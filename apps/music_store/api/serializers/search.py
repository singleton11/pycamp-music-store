from rest_framework import serializers

from apps.music_store.api.serializers import TrackSerializer, AlbumSerializer
from apps.music_store.models import Track, Album

SERIALIZER_MODELS = (
    (Track, TrackSerializer),
    (Album, AlbumSerializer),
)


class GlobalSearchSerializer(serializers.Serializer):
    """Serializer of queryset with objects mixed types"""
    def to_representation(self, obj):
        for model, serializer in SERIALIZER_MODELS:
            if not isinstance(obj, model):
                continue
            data = serializer(obj).data
            data['type'] = model.__name__
            return data

        raise TypeError("Object mot supported!")
