from rest_framework import exceptions
from rest_framework import viewsets, permissions, generics

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


class PaymentAccountView(generics.RetrieveUpdateAPIView):
    """ view for PaymentAccount. Support create, delete, edit methods """

    serializer_class = PaymentAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return PaymentAccount.objects.get(user=self.request.user)


class BoughtTrackViewSet(viewsets.ModelViewSet):
    """ View a list of bought tracks user and to buy the track. """
    serializer_class = BoughtTrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']
    queryset = BoughtTrack.objects.all()

    def get_queryset(self):
        user = self.request.user
        return BoughtTrack.objects.filter(user=user)

    def perform_create(self, serializer):
        """ Check, that user don't have selected track.

        Also check user balance, and subtract prise from balance.
        """
        user = self.request.user
        track = serializer.validated_data['track']
        if BoughtTrack.objects.filter(user=user, track=track).exists():
            # AlreadyExists
            raise exceptions.ValidationError('Track already bought')

        if not user.paymentaccount.pay_track(track):
            raise exceptions.ValidationError('You don\'t have money')

        # checking balance and price
        serializer.save(user=user)
