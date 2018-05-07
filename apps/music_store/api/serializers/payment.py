from rest_framework import serializers

from apps.music_store.models import (
    PaymentMethod,
    PaymentTransaction,
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

    purchase_type = serializers.SerializerMethodField()
    purchase_info = serializers.SerializerMethodField()
    purchase_id = serializers.SerializerMethodField()

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

    def get_purchase_type(self, obj):
        """Provide type of purchased good"""
        return str(obj.content_type)

    def get_purchase_info(self, obj):
        """Provide main info of purchased good"""
        return str(obj.content_object)

    def get_purchase_id(self, obj):
        """Provide id of purchased good"""
        return obj.object_id

