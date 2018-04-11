from rest_framework import serializers

from apps.music_store.models import LikeTrack, ListenTrack

__all__ = ('LikeTrackSerializer', 'ListenTrackSerializer',)


class LikeTrackSerializer(serializers.ModelSerializer):
    """Serializer for Likes of music tracks

    """
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = LikeTrack
        fields = (
            'id',
            'track',
            'user',
            'created',
        )


class ListenTrackSerializer(serializers.ModelSerializer):
    """Serializer for Listennings of Music tracks

    """
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = ListenTrack
        fields = (
            'id',
            'track',
            'user',
            'created',
        )
