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
from django.utils.translation import ugettext_lazy as _

admin.site.register(Album)
admin.site.register(BoughtAlbum)
admin.site.register(BoughtTrack)
admin.site.register(LikeTrack)
admin.site.register(ListenTrack)
admin.site.register(PaymentMethod)
admin.site.register(PaymentTransaction)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'album',
        'price',
    )
    list_per_page = 20
    search_fields = (
        'title',
        'author',
        'album',
    )
    ordering = ('title',)
    fieldsets = (
        (_('Main info'), {
            'fields': (
                'title',
                'author',
                'album',
                'price',
            )
        }),
        (_('Content'), {
            'fields': (
                'full_version',
                'free_version',
            )
        }),
    )
