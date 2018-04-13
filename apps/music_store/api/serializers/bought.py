from rest_framework import serializers

from ...models import BoughtAlbum, BoughtTrack

__all__ = ('BoughtTrackSerializer', 'BoughtAlbumSerializer',)


class BoughtItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('pk', 'user', 'item', 'created', 'transaction')


class BoughtTrackSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtTrack


class BoughtAlbumSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtAlbum
