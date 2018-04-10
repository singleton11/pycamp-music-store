from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel

from ..users.models import AppUser


class Album(
    TitleDescriptionModel,
    TimeStampedModel,
):
    """Music album with its title, image, price and related tracks.

    Attributes:
        title (str): text representation of album's title
        image (str): text representation of URL to album's image
        price (int): price of album. Minimal price is 0

    """
    image = models.CharField(
        verbose_name=_('Image'),
        max_length=200
    )
    price = models.BigIntegerField(
        verbose_name=_('Price'),
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('Music Album')
        verbose_name_plural = _('Music Albums')

    def __str__(self):
        return self.title

    @property
    def is_empty(self):
        """bool: True if no related Tracks"""
        return not self.tracks.exists()

    def buy_album(self, user):
        """Method to buy music track"""
        pass


class Track(
    TitleDescriptionModel,
    TimeStampedModel,
):
    """Music track with its title, price and album if exists.

    Attributes:
        title (str): text representation of track's title
        album (Album): album that contains the track
        price (int): price of album. Minimal price is 0
        full_version (str): full version of track content
        free_version (str): free shortened version of track content.
            Equal to full_version[:25]

    """
    album = models.ForeignKey(
        'Album',
        verbose_name=_('Album'),
        blank=True,
        null=True,
        related_name='tracks'
    )
    price = models.BigIntegerField(
        verbose_name=_('Price'),
        validators=[MinValueValidator(0)]
    )
    full_version = models.TextField(
        verbose_name=_('Full version'),
    )
    free_version = models.TextField(
        verbose_name=_('Free version'),
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('Audio Track')
        verbose_name_plural = _('Audio Tracks')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Saves reduced data to free_version field

        """
        self.free_version = self.full_version[:25]
        super().save(*args, **kwargs)


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


class LikeTrack(
    TimeStampedModel,
):
    """A 'Like' to music track.

    Unique pair of user who likes track and track, that is liked by user.

    """
    track = models.ForeignKey(
        Track,
        verbose_name=_('Track'),
    )
    user = models.ForeignKey(
        AppUser,
        verbose_name=_('User liked'),
    )

    class Meta:
        unique_together = (('track', 'user'),)
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class ListenTrack(
    TimeStampedModel,
):
    """A note about each listening of any track by any user.

    Each track may be listened multiple times.

    """
    track = models.ForeignKey(
        Track,
        verbose_name=_('Track'),
    )
    user = models.ForeignKey(
        AppUser,
        verbose_name=_('User listened'),
    )

    class Meta:
        verbose_name = _('Listen')
        verbose_name_plural = _('Listens')
