from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Track(TitleDescriptionModel):
    """ part of model for Track"""
    price = models.BigIntegerField(default=1, verbose_name=_('price'))

    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    def __str__(self):
        return self.title


class Album(models.Model):
    """ part of model for Album"""
    price = models.BigIntegerField(default=1, verbose_name=_('price'))

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')


class BoughtItem(TimeStampedModel):
    """ An abstract base class model for BoughtTrack and BoughtAlbum

    Attributes:
        user(AppUser): owner of item
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
    )

    class Meta:
        abstract = True
        unique_together = (('user', 'item'),)

    def __str__(self):
        return f'{self.user} bought {self.item}'


class BoughtTrack(BoughtItem):
    """Model for storing a bought track after purchase

    Attributes:
        item(Track): track purchased by the user
    """
    item = models.ForeignKey(
        'Track',
        verbose_name=_('track'),
        related_name='purchased',
    )

    class Meta(BoughtItem.Meta):
        verbose_name = _('Bought track')
        verbose_name_plural = _('Bought tracks')


class BoughtAlbum(BoughtItem):
    """Model for storing a bought albums after purchase

    Attributes:
        item(Album): album purchased by the user
    """
    item = models.ForeignKey(
        'Album',
        verbose_name=_('album'),
        related_name='purchased',
    )

    class Meta(BoughtItem.Meta):
        verbose_name = _('Bought album')
        verbose_name_plural = _('Bought albums')
