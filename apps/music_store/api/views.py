from rest_framework import viewsets
from apps.music_store.models import (
    MusicTrack,
    MusicAlbum,
    LikeTrack,
    ListenTrack,
)
from apps.music_store.api.serializers.music_albums_tracks import (
    MusicAlbumSerializer,
    MusicTrackSerializer,
    LikeTrackSerializer,
    ListenTrackSerializer,
)


# ##############################################################################
# MUSIC ALBUMS
# ##############################################################################


class AlbumViewSet(viewsets.ModelViewSet):
    """
    List all music labels, or create a new album.
    """
    queryset = MusicAlbum.objects.all()
    serializer_class = MusicAlbumSerializer


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class TrackViewSet(viewsets.ModelViewSet):
    """
    List all music labels, or create a new album.
    """
    queryset = MusicTrack.objects.all()
    serializer_class = MusicTrackSerializer


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class LikeTrackViewSet(viewsets.ModelViewSet):
    """
    List all music labels, or create a new album.
    """
    queryset = LikeTrack.objects.all()
    serializer_class = LikeTrackSerializer


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class ListenTrackViewSet(viewsets.ModelViewSet):
    """
    List all music labels, or create a new album.
    """
    queryset = ListenTrack.objects.all()
    serializer_class = ListenTrackSerializer

