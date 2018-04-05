from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel

from ..users.models import AppUser


class Album(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Music album with its title, image, price and related tracks.

    Attributes:
        title (CharField): text representation of album's title
        image (Charfield): text representation of URL to album's image
        price (FloatField): price of album. Minimal price is 0
    """
    image = models.CharField(
        verbose_name=_('Image'),
        max_length=200
    )
    price = models.FloatField(
        verbose_name=_('Price'),
        validators=[MinValueValidator(0.0)]
    )

    class Meta:
        ordering = ('created',)

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
    models.Model,
):
    """Music track with its title, price and album if exists.

    Attributes:
        title (CharField): text representation of track's title
        album (Album): album that contains the track
        price (FloatField): price of album. Minimal price is 0
    """
    album = models.ForeignKey(
        Album,
        verbose_name='Album',
        blank=True,
        null=True,
        related_name='tracks'
    )
    price = models.FloatField(
        verbose_name='Price',
        validators=[MinValueValidator(0.0)]
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def set_like(self, user):
        """Method to put like on track"""
        pass

    def del_like(self, user):
        """Method to take away like from track"""
        pass

    def play_track(self, user):
        """Method to play music track"""
        pass

    def buy_track(self, user):
        """Method to buy music track"""
        pass


class LikeTrack(
    TimeStampedModel,
    models.Model,
):
    """A 'Like' to music track.

    Unique pair of user who likes track and track, that is liked by user.
    """
    track = models.ForeignKey(Track)
    user = models.ForeignKey(AppUser)

    class Meta:
        unique_together = (('track', 'user'),)


class ListenTrack(
    TimeStampedModel,
    models.Model
):
    """A note about each listening of any track by any user.

    Each track may be listened multiple times.
    """
    track = models.ForeignKey(Track)
    user = models.ForeignKey(AppUser)
