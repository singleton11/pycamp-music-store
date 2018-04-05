from django.contrib import admin
from apps.music_store.models import (
    PaymentAccount,
    PaymentMethod,
    BoughtTrack,
    Track)

admin.site.register(PaymentAccount)
admin.site.register(PaymentMethod)
admin.site.register(BoughtTrack)
admin.site.register(Track)
