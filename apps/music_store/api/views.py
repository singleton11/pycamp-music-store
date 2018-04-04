from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from apps.music_store.api.serializers.music_albums_tracks import (
    LikeTrackSerializer,
    ListenTrackSerializer,
    AlbumSerializer,
    TrackSerializer,
)
from apps.music_store.models import (
    LikeTrack,
    ListenTrack,
    Album,
    Track,
)

# ##############################################################################
# MUSIC ALBUMS
# ##############################################################################


class AlbumViewSet(viewsets.ModelViewSet):
    """
    List all music albums, or create a new album.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class TrackViewSet(viewsets.ModelViewSet):
    """
    List all music tracks, or create a new track.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


# ##############################################################################
# Likes
# ##############################################################################


class LikeTrackViewSet(viewsets.ModelViewSet):
    """
    List all lokes for tracks.
    """
    queryset = LikeTrack.objects.all()
    serializer_class = LikeTrackSerializer


class LikeSomeTrackAPIView(
        generics.CreateAPIView,
        generics.DestroyAPIView,
        generics.GenericAPIView
):
    """
    List all music labels, or create a new album.
    """
    serializer_class = LikeTrackSerializer

    def create(self, request, *args, **kwargs):
        """Put a like to some track"""
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        user = self.request.user
        track_id = serializer.validated_data['track']

        like = LikeTrack(
            track=track_id,
            user=user,
        )
        like.save()

        return Response(
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Delete like from track"""
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        track_id = serializer.validated_data['track']
        user = self.request.user

        if LikeTrack.objects.get(pk=track_id, user=user):
            LikeTrack.objects.get(pk=track_id, user=user).delete()
        return Response(status=status.HTTP_200_OK)


# ##############################################################################
# Listens
# ##############################################################################


class ListenTrackViewSet(viewsets.ModelViewSet):
    """
    List all listens for tracks.
    """
    queryset = ListenTrack.objects.all()
    serializer_class = ListenTrackSerializer

