from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from apps.music_store.api.serializers import (
    AlbumSerializer,
    TrackSerializer,
    LikeTrackSerializer,
    ListenTrackSerializer,
    BoughtAlbumSerializer,
    BoughtTrackSerializer,
    PaymentAccountSerializer,
    PaymentMethodSerializer,
)
from apps.users.models import AppUser
from ...music_store.models import (
    Album,
    BoughtAlbum,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
    PaymentMethod,
    PaymentNotFound,
    NotEnoughMoney,
    ItemAlreadyBought
)


# ##############################################################################
# PAYMENT METHODS
# ##############################################################################

class PaymentMethodViewSet(viewsets.ModelViewSet):
    """ View for PaymentMethods """
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PaymentMethod.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# ##############################################################################
# ACCOUNTS
# ##############################################################################


class AccountView(generics.RetrieveUpdateAPIView):
    """ View for AppUser to work with balance and selected payment methods """

    serializer_class = PaymentAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AppUser.objects.all()

    def get_object(self):
        return super().get_queryset().get(pk=self.request.user.pk)


# ##############################################################################
# BOUGHT TRACKS
# ##############################################################################


class BoughtTrackViewSet(viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """View to display the list of purchased user tracks"""
    serializer_class = BoughtTrackSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BoughtTrack.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)


# ##############################################################################
# BOUGHT ALBUMS
# ##############################################################################


class BoughtAlbumViewSet(BoughtTrackViewSet):
    """View to display the list of purchased user albums"""
    serializer_class = BoughtAlbumSerializer
    queryset = BoughtAlbum.objects.all()


# ##############################################################################
# ITEMS
# ##############################################################################

class ItemViewSet(viewsets.mixins.ListModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    @detail_route(
        methods=['post'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='buy',
        url_name='buy',
    )
    def buy_album(self, request, **kwargs):
        """Method to buy item with using payment `payment_id`"""
        user = request.user
        item = self.get_object()
        payment_id = self.request.query_params.get('payment_id', None)

        try:
            payment_method = PaymentMethod.objects.get(
                owner=user,
                id=payment_id
            )
        except PaymentMethod.DoesNotExist:
            payment_method = None

        try:
            item.buy(user, payment_method)
        except (PaymentNotFound, NotEnoughMoney, ItemAlreadyBought) as e:
            return Response(
                data={'message': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_200_OK)


class AlbumViewSet(ItemViewSet):
    """Operations on music albums

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewSet(ItemViewSet):
    """Operations on music tracks

    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


# ##############################################################################
# LIKES
# ##############################################################################


class LikeTrackViewSet(viewsets.mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """Authorised user sees list of liked tracks.

    """
    queryset = LikeTrack.objects.all()
    serializer_class = LikeTrackSerializer
    permission_classes = (permissions.IsAuthenticated,)


# ##############################################################################
# LISTENS
# ##############################################################################


class ListenTrackViewSet(viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Authorised user sees list of listened tracks.

    """
    queryset = ListenTrack.objects.all()
    serializer_class = ListenTrackSerializer
    permission_classes = (permissions.IsAuthenticated,)
