from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill

from libs import utils

__all__ = [
    'AppUser',
]

# Solution to avoid unique_together for email
AbstractUser._meta.get_field('email')._unique = True


def upload_user_media_to(instance, filename):
    """Upload media files to this folder.

    Returns:
        String. Generated path for image.

    """
    return '{name}/{id}/{filename}'.format(
        name=instance.__class__.__name__.lower(),
        id=instance.id,
        filename=utils.get_random_filename(filename)
    )


class AppUser(AbstractUser):
    """Custom user model.

    Attributes:
        balance(BigInteger): current balance in cents.
        methods_used(PaymentMethod[]): saved payment methods
        default_method(PaymentMethod): default payment method
        avatar (file): user's avatar, cropeed to fill 300x300 px
        location (point): latest known GEO coordinates of the user
        location_updated (datetime): latest time user updated coordinates
        notifications (dict): settings for notifications to user
        first_name (str): first name
        last_name (str): last name
        username (str): username (not used)
        email (str): email (should be unique), this is our username field
        is_staff (bool): designates whether the user can log into
            this admin site
        is_active (bool): designates whether this user should be
            treated as active
        date_joined (datetime): when user joined
    """
    balance = models.BigIntegerField(
        default=0,
        verbose_name=_('balance'),
    )

    avatar = imagekitmodels.ProcessedImageField(
        upload_to=upload_user_media_to,
        processors=[ResizeToFill(300, 300)],
        format='PNG',
        options={'quality': 100},
        editable=False,
        null=True,
        blank=False
    )

    location = gis_models.PointField(
        default='POINT(0.0 0.0)',
        blank=True,
        srid=4326,
        editable=False
    )

    location_updated = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )

    notifications = HStoreField(null=True)

    # so authentication happens by email instead of username
    # and username becomes sort of nick
    USERNAME_FIELD = 'email'

    # Make sure to exclude email from required fields if authentication
    # is done by email
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def default_payment(self):
        q = self.payment_methods.filter(is_default=True)
        if q.exists():
            return q.first()
