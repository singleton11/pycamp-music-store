from rest_framework import serializers
import uuid

from apps.music_store.models import Album, Track

__all__ = (
    'AlbumSerializer',
    'TrackSerializer',
    'AdminTrackSerializer',
)


class IsBoughtMixin(serializers.BaseSerializer):
    """Mixin for check is_bought status of Album or Track"""

    def get_is_bought(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False

        user = request.user
        # always display as not bought for anonymous users
        if not user.is_authenticated:
            return False

        return obj.is_bought(user)


class AlbumSerializer(IsBoughtMixin, serializers.ModelSerializer):
    """Serializer for Music Albums

    """
    # all tracks related to the album
    tracks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Track.objects.all()
    )
    is_bought = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = (
            'id',
            'author',
            'title',
            'image',
            'price',
            'tracks',
            'is_bought',
        )


class TrackSerializer(IsBoughtMixin, serializers.ModelSerializer):
    """Serializer for Music Tracks"""

    is_liked = serializers.SerializerMethodField()
    count_likes = serializers.SerializerMethodField()
    is_bought = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Track
        fields = (
            'id',
            'author',
            'title',
            'album',
            'price',
            'is_bought',
            'is_liked',
            'count_likes',
            'content',
        )

    def get_content(self, obj):
        """Get name of free or full version of track.

        Full version is provided when track is bought by user.
        Otherwise free version is provided.

        Args:
            obj (Track): an instance of Track.

        """
        free_version = obj.free_version.url if obj.free_version else None
        full_version = obj.full_version.url if obj.full_version else None

        request = self.context.get('request')
        if not request:
            return free_version

        user = request.user
        if user.is_authenticated and obj.is_bought(user):
            return full_version
        return free_version

    def get_is_liked(self, obj):
        """Check if track is liked by authorized user"""
        request = self.context.get('request')
        if not request:
            return False

        user = request.user
        if not user.is_authenticated:
            return False

        return obj.is_liked(user)

    def get_count_likes(self, obj):
        """Get total number of 'likes' on the track"""
        request = self.context.get('request')
        if not request:
            return 0

        return obj.likes.count()


class AdminTrackSerializer(serializers.ModelSerializer):
    """Track serializer for admin to create, edit or delete the track"""
    # free_version = serializers.SerializerMethodField()
    # full_version = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = (
            'id',
            'author',
            'title',
            'album',
            'price',
            'free_version',
            'full_version',
        )

    # def get_free_version(self, obj):
    #     """Get url of free version of track"""
    #     return obj.free_version.url if obj.free_version else None
    #
    # def get_full_version(self, obj):
    #     """Get url of full version of track"""
    #     return obj.full_version.url if obj.full_version else None
