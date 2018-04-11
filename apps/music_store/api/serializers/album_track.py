from rest_framework import serializers

from apps.music_store.models import Album, Track, BoughtTrack


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for Music Albums

    """
    # all tracks related to the album
    tracks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Track.objects.all()
    )

    class Meta:
        model = Album
        fields = (
            'id',
            'author',
            'title',
            'image',
            'price',
            'tracks',
        )


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for Music Tracks"""

    content = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = (
            'id',
            'author',
            'title',
            'album',
            'price',
            'content',
        )

    def get_content(self, obj):
        """Get free or full version of track.

        Full version is provided when track is bought by user.
        Otherwise free version is provided.

        Args:
            obj (Track): an instance of Track.

        """
        request = self.context.get('request', None)
        if not request:
            return obj.free_version

        user = request.user
        if user.is_authenticated and obj.is_bought(user):
            return obj.full_version
        return obj.free_version

