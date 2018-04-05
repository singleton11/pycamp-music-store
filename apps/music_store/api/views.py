from rest_framework import viewsets, permissions, generics, status
from rest_framework import exceptions
from rest_framework.response import Response

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


class BoughtTrackView(generics.ListCreateAPIView):
    """ List Bought tracks of user. Support create, delete, edit methods """
    serializer_class = BoughtTrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return BoughtTrack.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        track = serializer.validated_data['track']
        if BoughtTrack.objects.filter(user=user, track=track).exists():
            # AlreadyExists
            raise exceptions.ValidationError('Track already bought')

        if user.paymentaccount.balance < track.track_price:
            raise exceptions.ValidationError('You don\'t have money')

        # checking balance and price
        serializer.save(user=user)
