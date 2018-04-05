from rest_framework import serializers

from ...models import BoughtTrack, BoughtAlbum


class BoughtTrackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = BoughtTrack
        fields = ('pk', 'user', 'track', 'date_purchase')


class BoughtAlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = BoughtAlbum
        fields = ('pk', 'user', 'album', 'date_purchase')
