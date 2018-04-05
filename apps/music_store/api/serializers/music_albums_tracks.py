from rest_framework import serializers

from apps.music_store.models import Album, LikeTrack, ListenTrack, Track


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for Music Albums

    """
    class Meta:
        model = Album
        fields = (
            'id',
            'album_name',
            'album_image',
            'album_price',
        )


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks

    """
    class Meta:
        model = Track
        fields = (
            'id',
            'track_name',
            'track_album',
            'track_price',
        )


class LikeTrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks

    """
    user = serializers.ReadOnlyField(source='user.pk')

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
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = ListenTrack
        fields = (
            'id',
            'track',
            'user',
            'listen_time',
        )
