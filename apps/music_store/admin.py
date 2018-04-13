from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea

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
admin.site.register(BoughtAlbum)
admin.site.register(BoughtTrack)
admin.site.register(LikeTrack)
admin.site.register(ListenTrack)
admin.site.register(PaymentMethod)
admin.site.register(PaymentTransaction)


class TrackAdminForm(forms.ModelForm):
    class Meta:
        model = Track
        widgets = {
            'full_version': Textarea(attrs={'rows': 2, 'cols': 79}),
            'free_version': Textarea(attrs={'rows': 1, 'cols': 79}),
        }
        fields = '__all__'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    form = TrackAdminForm

    list_display = (
        'title',
        'author',
        'album',
        'price',
    )
    list_per_page = 20
    list_filter = (
        'author',
        'album',
    )
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


class TrackInline(admin.TabularInline):
    model = Track
    form = TrackAdminForm
    fk_name = 'album'
    fields = (
        'title',
        'price',
        'full_version',
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = (
        TrackInline,
    )
    list_display = (
        'title',
        'author',
        'price',
    )
    list_per_page = 20
    search_fields = (
        'title',
        'author',
    )
    ordering = ('title',)
    fieldsets = (
        (_('Main info'), {
            'fields': (
                'title',
                'author',
                'image',
                'price',
            )
        }),
    )
