from rest_framework import serializers

from apps.music_store.models import (
    PaymentMethod,
    PaymentTransaction,
    BoughtTrack,
    BoughtAlbum,
)
from apps.music_store.api.serializers import (
    BoughtTrackSerializer,
    BoughtAlbumSerializer,
)
from apps.users.models import AppUser

__all__ = (
    'PaymentMethodSerializer',
    'PaymentAccountSerializer',
    'PaymentTransactionSerializer'
)


class PaymentMethodSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = PaymentMethod
        fields = ('owner', 'title', 'is_default')


class PaymentAccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    default_payment = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = (
            'user',
            'balance',
            'payment_methods',
            'default_payment',
        )

    def get_default_payment(self, obj):
        return obj.default_payment.pk


class PaymentTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    amount = serializers.ReadOnlyField()
    payment_method = PaymentMethodSerializer()
    created = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S'
    )
    purchased_track = serializers.SerializerMethodField()
    purchased_album = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTransaction
        fields = (
            'user',
            'amount',
            'payment_method',
            'created',
            'purchased_track',
            'purchased_album',
        )

    def get_purchased_track(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return None

        user = request.user

        track = BoughtTrack.objects.filter(transaction=obj, user=user)
        if track.exists():
            return BoughtTrackSerializer(track.get()).data
        return None

    def get_purchased_album(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return None

        user = request.user

        album = BoughtAlbum.objects.filter(transaction=obj, user=user)
        if album.exists():
            return BoughtAlbumSerializer(album.get()).data
        return None
