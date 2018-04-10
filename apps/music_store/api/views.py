from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, generics, exceptions

from apps.users.models import AppUser, PaymentMethod
from ...music_store.api.serializers.bought import (
    BoughtTrackSerializer,
    BoughtAlbumSerializer)
from ...music_store.api.serializers.payment import (
    PaymentAccountSerializer,
    PaymentMethodSerializer,
)
from ...music_store.models import (
    BoughtTrack,
    BoughtAlbum,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)

from apps.music_store.api.serializers import (
    AlbumSerializer,
    LikeTrackSerializer,
    ListenTrackSerializer,
    TrackSerializer,
)

from ...music_store.models import Album, LikeTrack, ListenTrack, Track



class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """ ReadOnly view for PaymentMethods """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class AccountView(generics.RetrieveUpdateAPIView):
    """ View for AppUser to work with balance and selected payment methods """

    serializer_class = PaymentAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AppUser.objects.all()

    def get_object(self):
        return super().get_queryset().get(pk=self.request.user.pk)


class BoughtTrackViewSet(viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """View to display the list of purchased user tracks and purchase them."""
    serializer_class = BoughtTrackSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BoughtTrack.objects.all()

    def filter_queryset(self, queryset):
        user = self.request.user
        return super().filter_queryset(queryset).filter(user=user)

    def perform_create(self, serializer):
        """ Pay for item and save bought item """
        user = self.request.user
        item = serializer.validated_data['item']
        try:
            user.pay_item(item)
        except ValidationError as e:
            raise exceptions.ValidationError(e.message)

        serializer.save()


class BoughtAlbumViewSet(BoughtTrackViewSet):
    """View to display the list of purchased user albums and purchase them."""
    serializer_class = BoughtAlbumSerializer
    queryset = BoughtAlbum.objects.all()


# ##############################################################################
# MUSIC ALBUMS
# ##############################################################################


class AlbumViewSet(viewsets.ModelViewSet):
    """Operations on music albums

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ##############################################################################
# MUSIC TRACKS
# ##############################################################################


class TrackViewSet(viewsets.ModelViewSet):
    """Operations on music tracks

    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ##############################################################################
# Likes
# ##############################################################################


class LikeTrackViewSet(viewsets.ModelViewSet):
    """List likes for all music tracks and users.

    """
    queryset = LikeTrack.objects.all()
    serializer_class = LikeTrackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """Put a Like to some track.

        Allows to save Like only to logged user

        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Put away Like from the track.

        Allows to destroy Like only to user who put that like

        """
        if self.request.user == instance.user:
            instance.delete()


# ##############################################################################
# Listens
# ##############################################################################


class ListenTrackViewSet(viewsets.ModelViewSet):
    """List all listens of all tracks by current user.

    """
    queryset = ListenTrack.objects.all()
    serializer_class = ListenTrackSerializer
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'head']

    def perform_create(self, serializer):
        """Put a Like to some track.

        Allows to save Like only to logged user

        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Show user his history of listening"""
        return ListenTrack.objects.filter(user=self.request.user)
