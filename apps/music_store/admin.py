from django.contrib import admin

from apps.music_store.models import (
    BoughtTrack,
    Track
)
from apps.users.models import PaymentMethod, PaymentTransaction

admin.site.register(PaymentMethod)
admin.site.register(BoughtTrack)
admin.site.register(Track)
admin.site.register(PaymentTransaction)
