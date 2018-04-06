from rest_framework import viewsets, permissions, generics

from apps.users.models import AppUser, PaymentMethod
from ...music_store.api.serializers.bought import (
    BoughtTrackSerializer,
)
from ...music_store.api.serializers.payment import (
    PaymentAccountSerializer,
    PaymentMethodSerializer,
)
from ...music_store.models import (
    BoughtTrack,
    BoughtAlbum,
)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """ ReadOnly view for PaymentMethods """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class AccountView(generics.RetrieveUpdateAPIView):
    """ View for PaymentAccount. Support read and update """

    serializer_class = PaymentAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return AppUser.objects.get(pk=self.request.user.pk)


class BoughtTrackViewSet(viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """ View a list of bought users tracks and can buy the track."""
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
        user.pay_item(item)
        serializer.save()


class BoughtAlbumViewSet(BoughtTrackViewSet):
    """ View a list of bought albums user and can buy the album. """
    queryset = BoughtAlbum.objects.all()
