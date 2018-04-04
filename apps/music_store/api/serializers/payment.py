from rest_framework import serializers

from apps.music_store.models import PaymentMethod, PaymentAccount, BoughtTrack


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title',)


class PaymentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAccount
        fields = ('user', 'balance', 'methods_used', 'default_method')


class BoughtTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoughtTrack
        fields = ('user', 'track', 'date_purchase')
