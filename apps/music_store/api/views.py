from rest_framework import viewsets, permissions

from ...music_store.api.serializers.payment import (
    PaymentAccountSerializer,
    PaymentMethodSerializer,
    BoughtTrackSerializer)
from ...music_store.models import (
    PaymentAccount,
    PaymentMethod,
    BoughtTrack)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """ ReadOnly view for PaymentMethods """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """ view for PaymentAccount. Support create, delete, edit methods """
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class BoughtTrackViewSet(viewsets.ReadOnlyModelViewSet):
    """ view for BoughtTrack. Support create, delete, edit methods """
    queryset = BoughtTrack.objects.all()
    serializer_class = BoughtTrackSerializer
    permission_classes = [permissions.IsAuthenticated]
