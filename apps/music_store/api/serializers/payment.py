from rest_framework import serializers

from apps.music_store.models import PaymentMethod
from apps.users.models import AppUser

__all__ = ('PaymentMethodSerializer', 'PaymentAccountSerializer',)


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
