from rest_framework import serializers

from ...models import BoughtTrack, BoughtAlbum


class BoughtTrackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = BoughtTrack
        fields = ('pk', 'user', 'item', 'created')


class BoughtAlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = BoughtAlbum
        fields = ('pk', 'user', 'item', 'created')
