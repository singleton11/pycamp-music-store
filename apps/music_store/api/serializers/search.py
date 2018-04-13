from rest_framework import serializers

from apps.music_store.api.serializers import TrackSerializer, AlbumSerializer


class GlobalSearchSerializer(serializers.Serializer):
    tracks = TrackSerializer(many=True)
    albums = AlbumSerializer(many=True)
