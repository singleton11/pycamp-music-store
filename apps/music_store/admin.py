from django.contrib import admin

from apps.music_store.models import (
    Album,
    BoughtAlbum,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
)
from apps.users.models import PaymentMethod, PaymentTransaction

admin.site.register(Album)
admin.site.register(BoughtAlbum)
admin.site.register(BoughtTrack)
admin.site.register(LikeTrack)
admin.site.register(ListenTrack)
admin.site.register(PaymentMethod)
admin.site.register(PaymentTransaction)
admin.site.register(Track)
