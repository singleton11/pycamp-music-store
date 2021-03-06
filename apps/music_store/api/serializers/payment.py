from rest_framework import serializers

from apps.music_store.models import (
    PaymentMethod,
    PaymentTransaction,
)
from apps.users.models import AppUser

__all__ = (
    'PaymentMethodSerializer',
    'PaymentAccountSerializer',
    'PaymentTransactionSerializer',
)


class PaymentMethodSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = PaymentMethod
        fields = (
            'id',
            'owner',
            'title',
            'is_default',
        )


class PaymentAccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    email = serializers.EmailField()

    class Meta:
        model = AppUser
        fields = (
            'user',
            'email',
            'balance',
        )


class PaymentTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    amount = serializers.ReadOnlyField()
    payment_method = PaymentMethodSerializer()
    created = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S'
    )

    class Meta:
        model = PaymentTransaction
        fields = (
            'user',
            'amount',
            'payment_method',
            'created',
            'purchase_type',
            'purchase_info',
            'purchase_id',
        )
