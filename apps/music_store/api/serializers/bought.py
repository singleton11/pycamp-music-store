from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.users.models import PaymentMethod
from ...models import BoughtTrack, BoughtAlbum


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('pk', 'title',)


class BoughtItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('pk', 'user', 'item', 'created')


class BoughtTrackSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtTrack
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'item'),
                message='Track already bought'
            )
        ]


class BoughtAlbumSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtAlbum
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'item'),
                message='Album already bought'
            )
        ]
