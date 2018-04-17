from django import forms
from django.contrib import admin
from django.forms.widgets import Textarea
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from apps.music_store.models import (
    Album,
    BoughtAlbum,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
    PaymentTransaction,
    PaymentMethod,
)

admin.site.register(PaymentMethod)
admin.site.register(PaymentTransaction)


class TrackAdminForm(forms.ModelForm):
    """Custom form to display Track with small text boxes for 'full_version' and
    'free_Version' fields.

    """
    class Meta:
        model = Track
        widgets = {
            'full_version': Textarea(attrs={'rows': 2, 'cols': 50}),
            'free_version': Textarea(attrs={'rows': 1, 'cols': 50}),
        }
        fields = '__all__'


class TrackInline(admin.TabularInline):
    """Inline Track to display list of tracks inside Album."""
    model = Track
    form = TrackAdminForm
    fk_name = 'album'
    fields = (
        'title',
        'price',
        'full_version',
    )


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    """Custom form for Tracks"""
    form = TrackAdminForm
    # List display
    list_display = (
        'title',
        'author',
        'album',
        'price',
    )
    list_filter = (
        'author',
        'album',
    )
    list_per_page = 20
    ordering = ('title',)
    search_fields = (
        'title',
        'author',
        'album',
    )
    # Single Track display
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

    change_list_template = 'music_store/track/change_list.html'

    def get_urls(self):
        from django.conf.urls import url
        urls = super(TrackAdmin, self).get_urls()
        my_urls = [
            url(r'^upload_archive/$',  self.admin_site.admin_view(self.my_view)),
        ]
        return my_urls + urls

    def my_view(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           denis="super",
        )
        return TemplateResponse(request, "music_store/upload_archive.html", context)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Custom form for Albums"""
    # List display
    inlines = (
        TrackInline,
    )
    list_display = (
        'title',
        'author',
        'price',
    )
    list_filter = (
        'author',
    )
    list_per_page = 20
    ordering = ('title',)
    search_fields = (
        'title',
        'author',
    )
    # Single Track display
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


@admin.register(LikeTrack)
class LikeTrackAdmin(admin.ModelAdmin):
    """Custom form for Likes"""
    list_display = (
        'user',
        'track',
        'created',
    )
    list_filter = (
        'created',
    )
    search_fields = (
        'track',
        'user',
    )
    list_per_page = 20
    ordering = ('created',)


@admin.register(ListenTrack)
class ListenTrackAdmin(admin.ModelAdmin):
    """Custom form for Listens"""
    list_display = (
        'user',
        'track',
        'created',
    )
    list_filter = (
        'created',
    )
    search_fields = (
        'track',
        'user',
    )
    list_per_page = 20
    ordering = ('created',)


@admin.register(BoughtAlbum)
class BoughtAlbumAdmin(admin.ModelAdmin):
    """Custom form for Bought albums"""
    list_display = (
        'user',
        'item',
        'created',
    )
    list_filter = (
        'created',
    )
    search_fields = (
        'item',
        'user',
    )
    list_per_page = 20
    ordering = ('created',)


@admin.register(BoughtTrack)
class BoughtTrackAdmin(admin.ModelAdmin):
    """Custom form for Bought tracks"""
    list_display = (
        'user',
        'item',
        'created',
    )
    list_filter = (
        'created',
    )
    search_fields = (
        'item',
        'user',
    )
    list_per_page = 20
    ordering = ('created',)
