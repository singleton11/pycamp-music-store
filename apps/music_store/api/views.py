from rest_framework import viewsets

from apps.music_store.api.serializers.payment import (
    PaymentAccountSerializer,
    PaymentMethodSerializer,
    BoughtTrackSerializer)
from apps.music_store.models import (
    PaymentAccount,
    PaymentMethod,
    BoughtTrack)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentAccountViewSet(viewsets.ModelViewSet):
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountSerializer


class BoughtTrackViewSet(viewsets.ModelViewSet):
    queryset = BoughtTrack.objects.all()
    serializer_class = BoughtTrackSerializer
