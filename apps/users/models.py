from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import HStoreField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill

from libs import utils

__all__ = [
    'AppUser',
    'PaymentMethod',
    'PaymentTransaction'
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


class PaymentMethod(models.Model):
    """Model to store payment methods."""
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')

    def __str__(self):
        return self.title


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

    methods_used = models.ManyToManyField(
        PaymentMethod,
        related_name='users',
        verbose_name=_('methods used'),
    )
    default_method = models.ForeignKey(
        PaymentMethod,
        related_name='users_by_default',
        null=True,
        verbose_name=_('default method'),
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

    def pay_item(self, item):
        """ Method for subtract cost of item.

        Raises:
            exceptions.ValidationError: User does not have enough money
        """
        if not self.can_pay(item.price):
            raise ValidationError("Not enough money")

        # create new negative transaction
        PaymentTransaction.objects.create(
            user=self,
            amount=-item.price,
        )

    def can_pay(self, amount):
        """ Checking that user have 'amount' of money"""
        return self.balance >= amount

    def check_default_method(self):
        """ Checking that default method in methods_used """
        return self.default_method in self.methods_used.all()

    def update_balance(self):
        """ Method to recalculated user balance. """
        self.balance = PaymentTransaction.objects \
            .filter(user=self) \
            .aggregate(total_amount=Sum('amount')).get('total_amount')

        self.save(update_fields=['balance'])
        self.refresh_from_db()


class PaymentTransaction(TimeStampedModel):
    """Model for storing operations with user balance """

    user = models.ForeignKey(AppUser, verbose_name=_('user'))
    amount = models.BigIntegerField(verbose_name=_('amount'))
    payment_method = models.ForeignKey(
        PaymentMethod,
        blank=True,
        null=True,
        verbose_name=_('payment method')
    )

    class Meta:
        verbose_name = _('Payment transaction')
        verbose_name_plural = _('Payment transactions')

    def save(self, **kwargs):
        if self.amount < 0 and not self.user.can_pay(-self.amount):
            raise ValidationError("Not enough money")
        super().save(**kwargs)
        # after creating a new transaction, the user balance will be updated
        self.user.update_balance()

    def __str__(self):
        if self.amount < 0:
            return f'{self.user} has spent {-self.amount}'
        return f'{self.user} received {self.amount}'
