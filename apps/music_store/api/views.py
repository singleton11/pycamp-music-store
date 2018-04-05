from rest_framework import viewsets

from apps.music_store.api.serializers.music_albums_tracks import (
    AlbumSerializer,
    LikeTrackSerializer,
    ListenTrackSerializer,
    TrackSerializer,
)
from apps.music_store.models import Album, LikeTrack, ListenTrack, Track

# ##############################################################################
# MUSIC ALBUMS
# ##############################################################################


class AlbumViewSet(viewsets.ModelViewSet):
    """List all music albums, or create a new album.

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    # http_method_names = ['get', 'head']


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class TrackViewSet(viewsets.ModelViewSet):
    """List all music tracks, or create a new track.

    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    # http_method_names = ['get', 'head']


# ##############################################################################
# Likes
# ##############################################################################


class LikeTrackViewSet(viewsets.ModelViewSet):
    """List likes for all music tracks and users.

    """
    queryset = LikeTrack.objects.all()
    serializer_class = LikeTrackSerializer

    def perform_create(self, serializer):
        """Put a Like to some track.

        Allows to save Like only to logged user"""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Put away Like from the track.

        Allows to destroy Like only to user who put that like"""
        if self.request.user == instance.user:
            instance.delete()

    # def get_queryset(self):
    #     return LikeTrack.objects.filter(user=self.request.user)


# ##############################################################################
# Listens
# ##############################################################################


class ListenTrackViewSet(viewsets.ModelViewSet):
    """List all listens of all tracks by current user.

    """
    queryset = ListenTrack.objects.all()
    serializer_class = ListenTrackSerializer

    http_method_names = ['get', 'post', 'head']

    def perform_create(self, serializer):
        """Put a Like to some track.

        Allows to save Like only to logged user"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Show user his history of listening"""
        return ListenTrack.objects.filter(user=self.request.user)
