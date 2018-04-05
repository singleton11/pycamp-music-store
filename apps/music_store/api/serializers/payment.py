from rest_framework import serializers

from ...models import PaymentMethod, PaymentAccount


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title',)


class PaymentAccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = PaymentAccount
        fields = ('user', 'balance', 'methods_used', 'default_method')
