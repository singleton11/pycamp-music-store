from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from django.db import IntegrityError

from ..users.models import AppUser


class LikeAlreadyExistsError(IntegrityError):
    """Error when user try to like track that is already liked."""
    pass


class LikeNotExistsError(IntegrityError):
    """Error when user try to remove like from track that is not liked."""
    pass


class MusicItem(
    TitleDescriptionModel,
    TimeStampedModel,
):
    """Abstract base class for Album and Track.

    Attributes:
        title (str): text representation of items's title.
        author (str): text representation of author's name.
        price (int): price of item. Minimal price is 0.

    """
    author = models.CharField(
        verbose_name=_('Author'),
        blank=True,
        null=True,
        max_length=200,
    )

    price = models.BigIntegerField(
        verbose_name=_('Price'),
        validators=[MinValueValidator(0)]
    )

    class Meta:
        abstract = True
        ordering = ('created',)

    def __str__(self):
        return f'{self.author} - {self.title}'


class Album(MusicItem):
    """Music album with its title, image, price and related tracks.

    Attributes:
        image (str): text representation of URL to album's image.

    Properties:
        is_empty (bool): True if album does not have related tracks.

    """
    image = models.CharField(
        verbose_name=_('Image'),
        max_length=200
    )

    class Meta(MusicItem.Meta):
        verbose_name = _('Music Album')
        verbose_name_plural = _('Music Albums')

    @property
    def is_empty(self):
        """bool: True if no related Tracks"""
        return not self.tracks.exists()

    def is_bought(self, user):
        """Check if the album is bought by the user.

        Args:
            user (AppUser): probable owner of album.

        """
        return BoughtAlbum.objects.filter(user=user, item=self).exists()


class Track(MusicItem):
    """Music track with its title, price and album if exists.

    Attributes:
        album (Album): album that contains the track.
        full_version (str): full version of track content.
        free_version (str): free shortened version of track content.
            Equal to full_version[:25].

    """
    album = models.ForeignKey(
        'Album',
        verbose_name=_('Album'),
        blank=True,
        null=True,
        related_name='tracks'
    )
    full_version = models.TextField(
        verbose_name=_('Full version'),
    )
    free_version = models.TextField(
        verbose_name=_('Free version'),
    )

    class Meta(MusicItem.Meta):
        verbose_name = _('Audio Track')
        verbose_name_plural = _('Audio Tracks')

    def save(self, *args, **kwargs):
        """Saves reduced data to free_version field.

        """
        self.free_version = self.full_version[:25]
        super().save()

    def is_bought(self, user):
        """Check if the track is bought by the user.

        Args:
            user (AppUser): probable owner of track.

        """
        return BoughtTrack.objects.filter(user=user, item=self).exists()

    def is_liked(self, user):
        """Check if the track is liked by the user.

        Args:
            user (AppUser): probable owner of track.

        """
        return LikeTrack.objects.filter(user=user, track=self).exists()

    def like(self, user):
        """Create 'Like' for the track by some user.

        Args:
            user (AppUser): user who likes the track.

        """
        if self.is_liked(user):
            raise LikeAlreadyExistsError('Track is already liked!')

        return LikeTrack.objects.create(user=user, track=self)

    def unlike(self, user):
        """Remove 'Like' from the track by some user.

        Args:
            user (AppUser): user who removes like from the track.

        """
        if not self.is_liked(user):
            raise LikeNotExistsError('Track is not liked!')

        return LikeTrack.objects.filter(user=user, track=self).delete()

    def listen(self, user):
        """Note about the track was listened by some user

        Args:
            user (AppUser): user who listened to the track.

        """
        return ListenTrack.objects.create(user=user, track=self)


class BoughtItem(TimeStampedModel):
    """ An abstract base class model for BoughtTrack and BoughtAlbum.

    Attributes:
        user(AppUser): owner of item.
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
