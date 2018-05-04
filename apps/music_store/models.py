from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel

from apps.music_store.exceptions import PaymentNotFound, NotEnoughMoney, \
    ItemAlreadyBought


class PaymentMethod(models.Model):
    """Model to store payment methods."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='payment_methods',
    )
    title = models.CharField(max_length=100)
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is default'),
    )

    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')

    def __str__(self):
        return f'{self.owner}\'s method {self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if this method is default, set all other methods not default
        if self.is_default:
            default_methods = PaymentMethod.objects.filter(
                owner=self.owner,
                is_default=True,
            )
            default_methods.exclude(pk=self.pk).update(is_default=False)


class PaymentTransaction(TimeStampedModel):
    """Model for storing operations with user balance """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='transactions',
    )
    amount = models.BigIntegerField(verbose_name=_('amount'))
    payment_method = models.ForeignKey(
        'PaymentMethod',
        blank=True,
        null=True,
        verbose_name=_('payment method'),
        related_name='transactions',
    )

    class Meta:
        verbose_name = _('Payment transaction')
        verbose_name_plural = _('Payment transactions')

    def __str__(self):
        if self.amount < 0:
            return f'{self.user} has spent {abs(self.amount)}'
        return f'{self.user} received {self.amount}'

    def update_user_balance(self, user):
        """ Method for update user balance """
        total_balance = self.__class__.objects.filter(user=user) \
            .aggregate(total_amount=Sum('amount')) \
            .get('total_amount')

        user.balance = total_balance
        user.save(update_fields=['balance'])
        user.refresh_from_db()

    def save(self, **kwargs):
        if self.amount < 0 and self.user.balance < abs(self.amount):
            raise NotEnoughMoney

        super().save(**kwargs)
        self.update_user_balance(self.user)


class MusicItem(TitleDescriptionModel, TimeStampedModel):
    """Abstract base class for Album and Track.

    Attributes:
        title (str): text representation of items's title.
        author (str): text representation of author's name.
        price (int): price of item. Minimal price is 0.

    """
    author = models.CharField(
        verbose_name=_('author'),
        blank=True,
        null=True,
        max_length=200,
    )

    price = models.BigIntegerField(
        verbose_name=_('price'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        ordering = ('created',)

    def __str__(self):
        return f'{self.author} - {self.title}'

    @property
    def bought_model(self):
        """Returns the corresponding model of purchased items"""
        types = {
            Album: BoughtAlbum,
            Track: BoughtTrack,
        }
        return types.get(self.__class__)

    def is_bought(self, user):
        """Check if the track is bought by some user.

        Args:
            user (AppUser): probable owner of track.

        """
        return self.bought_model.objects.filter(user=user, item=self).exists()

    def buy(self, user, payment_method=None):
        """ Method for buy this item

        Raises:
            exceptions.ValidationError: User does not have enough money
            exceptions.ValidationError: User don't have payment method
        """

        payment_method = payment_method or user.default_payment

        if payment_method is None:
            raise PaymentNotFound

        if user.balance < self.price:
            raise NotEnoughMoney

        if self.bought_model.objects.filter(user=user, item=self).exists():
            raise ItemAlreadyBought

        transaction = PaymentTransaction.objects.create(
            user=user,
            amount=-self.price,
            payment_method=payment_method,
        )
        self.bought_model.objects.create(
            user=user,
            item=self,
            transaction=transaction,
        )


class Album(MusicItem):
    """Music album with its title, image, price and related tracks.

    Attributes:
        image (str): text representation of URL to album's image.

    Properties:
        is_empty (bool): True if album does not have related tracks.

    """
    bought_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through='BoughtAlbum',
                                          related_name='albums')
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


class Track(MusicItem):
    """Music track with its title, price and album if exists.

    Attributes:
        album (Album): album that contains the track.
        full_version (str): full version of track content.
        free_version (str): free shortened version of track content.
            Equal to full_version[:25].

    """
    bought_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BoughtTrack',
        related_name='tracks'
    )
    album = models.ForeignKey(
        'Album',
        verbose_name=_('album'),
        blank=True,
        null=True,
        related_name='tracks'
    )
    full_version = models.TextField(
        verbose_name=_('full version'),
    )
    free_version = models.TextField(
        verbose_name=_('free version'),
        default='free version'
    )

    class Meta(MusicItem.Meta):
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    def save(self, *args, **kwargs):
        """Saves reduced data to free_version field.

        """
        self.free_version = self.full_version[:25]
        super().save(*args, **kwargs)

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
        if not self.is_liked(user):
            return LikeTrack.objects.create(user=user, track=self)

    def unlike(self, user):
        """Remove 'Like' from the track by some user.

        Args:
            user (AppUser): user who removes like from the track.

        """
        if self.is_liked(user):
            return LikeTrack.objects.filter(user=user, track=self).delete()

    def listen(self, user):
        """Note about the track was listened by some user

        Args:
            user (AppUser): user who listened to the track.

        """
        return ListenTrack.objects.create(user=user, track=self)

    def is_bought(self, user):
        """Note about the track was listened by some user

        Args:
            user (AppUser): user

        """

        if super().is_bought(user):
            return True

        return self.album and self.album.is_bought(user)


class BoughtItem(TimeStampedModel):
    """ An abstract base class model for BoughtTrack and BoughtAlbum.

    Attributes:
        user(AppUser): owner of item.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
    )
    transaction = models.ForeignKey(
        'PaymentTransaction',
        verbose_name=_('transaction'),
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


class LikeTrack(TimeStampedModel):
    """A 'Like' to music track.

    Unique pair of user who likes track and track, that is liked by user.

    """
    track = models.ForeignKey(
        Track,
        verbose_name=_('track'),
        related_name='likes',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('liked by'),
        related_name='likes',
    )

    class Meta:
        unique_together = (('track', 'user'),)
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f'{self.user} liked {self.track}'


class ListenTrack(TimeStampedModel):
    """A note about each listening of any track by any user.

    Each track may be listened multiple times.

    """
    track = models.ForeignKey(
        Track,
        verbose_name=_('track'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Listened by'),
    )

    class Meta:
        verbose_name = _('Listen')
        verbose_name_plural = _('Listens')

    def __str__(self):
        return f'{self.user} listened {self.track}'
