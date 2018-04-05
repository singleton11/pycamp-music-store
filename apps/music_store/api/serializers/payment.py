from rest_framework import serializers

from apps.users.models import AppUser, PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title',)
        fields = ('title',)


class PaymentAccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = AppUser
        fields = (
            'user',
            'balance',
            'methods_used',
            'default_method',
        )
