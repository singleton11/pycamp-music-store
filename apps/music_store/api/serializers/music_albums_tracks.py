from rest_framework import serializers
from apps.users.models import AppUser
from apps.music_store.models import MusicAlbum, MusicTrack, LikeTrack, ListenTrack


class MusicAlbumSerializer(serializers.ModelSerializer):
    """Serializer for Music Albums

    """
    class Meta:
        model = MusicAlbum
        fields = (
            'id',
            'album_name',
            'album_image',
            'album_price',
        )


class MusicTrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks

    """
    class Meta:
        model = MusicTrack
        fields = (
            'id',
            'track_name',
            'track_album',
            'track_price',
        )


class LikeTrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks

    """
    class Meta:
        model = LikeTrack
        fields = (
            'id',
            'track',
            'user',
            'like_time',
        )


class ListenTrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks

    """
    class Meta:
        model = ListenTrack
        fields = (
            'id',
            'track',
            'user',
            'listen_time',
        )

