from rest_framework import exceptions, serializers

from apps.users.models import AppUser, PaymentMethod

__all__ = ('PaymentMethodSerializer', 'PaymentAccountSerializer',)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title',)


class PaymentAccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = AppUser
        fields = (
            'user',
            'balance',
            'methods_used',
            'default_method',
        )

    def validate(self, attrs):
        # check that the Default method belongs to the methods used
        default_method = attrs.get('default_method', None)
        if default_method not in attrs.get('methods_used', []):
            raise exceptions.ValidationError(
                "The default method must belong to methods used"
            )
        return super().validate(attrs)
