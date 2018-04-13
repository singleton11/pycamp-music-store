from rest_framework import serializers

from apps.music_store.models import PaymentMethod
from ...models import BoughtAlbum, BoughtTrack

__all__ = ('BoughtTrackSerializer', 'BoughtAlbumSerializer',)


class BoughtItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    payment = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        required=False,
    )

    class Meta:
        fields = ('pk', 'user', 'item', 'created', 'payment', 'transaction')


class BoughtTrackSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtTrack


class BoughtAlbumSerializer(BoughtItemSerializer):
    class Meta(BoughtItemSerializer.Meta):
        model = BoughtAlbum
