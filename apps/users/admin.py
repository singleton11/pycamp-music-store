from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.music_store.admin import (
    PaymentMethodInline,
    PaymentTransactionInline,
)
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    inlines = (PaymentMethodInline, PaymentTransactionInline)

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password'
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                '_avatar'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
        (_('Location'), {
            'fields': (
                '_location',
                '_location_updated'
            )
        }),
        (_('Notifications'), {
            'fields': (
                'notifications',
            )
        }),
        (_('Payment'), {
            'fields': (
                'balance',
            )
        })
    )
    readonly_fields = UserAdmin.readonly_fields + (
        '_avatar',
        '_location',
        '_location_updated',
        'notifications',
    )

    def _payment_methods(self, user):
        return user.payment_methods

    def _default_payment(self, user):
        return user.default_payment

    def _avatar(self, user):
        if user.avatar:
            return format_html(mark_safe(
                "<img src='{}' >".format(user.avatar.url)))
        else:
            return "None"

    _avatar.short_description = "Avatar"

    def _location(self, user):
        lon, lat = user.location
        url = 'http://maps.google.com/maps?t=h&q=loc:{},{},10z'.format(
            lat, lon)
        link = format_html("<a href='{0}'>{1}, {2}</a>", url, lat, lon)
        return link

    _location.short_description = 'Coordinates (latitude, longitude)'

    def _location_updated(self, user):
        return user.location_updated

    _location_updated.short_description = 'Location updated'
