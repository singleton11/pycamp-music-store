from rest_framework import viewsets, permissions, generics

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
        user.pay_item(item)
        serializer.save()


class BoughtAlbumViewSet(BoughtTrackViewSet):
    """View to display the list of purchased user albums and purchase them."""
    serializer_class = BoughtAlbumSerializer
    queryset = BoughtAlbum.objects.all()
