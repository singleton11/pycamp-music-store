from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ...models import BoughtTrack, BoughtAlbum


class BoughtTrackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = BoughtTrack
        fields = ('pk', 'user', 'item', 'created')

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'item'),
                message='Track already bought'
            )
        ]


class BoughtAlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = BoughtAlbum
        fields = ('pk', 'user', 'item', 'created')

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'item'),
                message='Album already bought'
            )
        ]
