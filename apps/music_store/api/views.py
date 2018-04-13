import coreapi
import coreschema
from django.db.models import Q
from rest_framework import exceptions, generics, permissions, viewsets, \
    filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

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
from apps.music_store.api.serializers.search import GlobalSearchSerializer
from apps.users.models import AppUser
from ...music_store.models import (
    Album,
    BoughtAlbum,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
    PaymentMethod,
    NotEnoughMoney,
    PaymentNotFound
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


class BoughtTrackViewSet(viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """View to display the list of purchased user tracks and purchase them."""
    serializer_class = BoughtTrackSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BoughtTrack.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)

    def perform_create(self, serializer):
        """ Pay for item and save bought item """
        user = self.request.user
        item = serializer.validated_data.get('item')
        payment_method = serializer.validated_data.get('payment')

        try:
            item.buy(user, payment_method)
        except (PaymentNotFound, NotEnoughMoney)  as e:
            raise exceptions.ValidationError(e.message)

        serializer.save()


# ##############################################################################
# BOUGHT ALBUMS
# ##############################################################################


class BoughtAlbumViewSet(BoughtTrackViewSet):
    """View to display the list of purchased user albums and purchase them."""
    serializer_class = BoughtAlbumSerializer
    queryset = BoughtAlbum.objects.all()


# ##############################################################################
# ALBUMS
# ##############################################################################


class AlbumViewSet(viewsets.mixins.ListModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """Operations on music albums

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'author',)


# ##############################################################################
# TRACKS
# ##############################################################################


class TrackViewSet(viewsets.mixins.ListModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """Operations on music tracks

    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'author',)


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


# ##############################################################################
# SEARCH
# ##############################################################################


class GlobalSearchList(APIView):
    """View for global searching.

    Search Tracks and Albums, which contain the value of get-parameter "query"
    in the "title" or "author" fields.

    """
    search_param = 'query'

    def get(self, request):
        query = request.query_params.get(self.search_param, None)
        if not query:
            message = f"Query parameter '{self.search_param}' is required"
            raise ValidationError(message)

        search_filter = Q(author__icontains=query) | Q(title__icontains=query)
        tracks = Track.objects.filter(search_filter)
        albums = Album.objects.filter(search_filter)
        result = GlobalSearchSerializer({'tracks': tracks, 'albums': albums})
        return Response(data=result.data, status=status.HTTP_201_CREATED)

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=self.search_param,
                required=True,
                location='query',
                schema=coreschema.String(
                    title="The string to search",
                    description="The string that will be used to "
                                "search in the fields"
                )
            )
        ]
