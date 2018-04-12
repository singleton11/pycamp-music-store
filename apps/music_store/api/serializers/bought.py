from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.music_store.models import PaymentMethod
from ...models import BoughtAlbum, BoughtTrack


class BoughtItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    payment = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        required=False,
    )

    class Meta:
        fields = ('pk', 'user', 'item', 'created', 'payment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        user = request.user
        qs = self.fields['payment'].queryset
        self.fields['payment'].queryset = qs.filter(owner=user)


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
