from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill
from rest_framework import exceptions

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

    def __str__(self):
        return self.title


class AppUser(AbstractUser):
    """Custom user model.

    Attributes:
        balance(float): current balance.
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

    balance = models.DecimalField(
        default=0,
        max_digits=16,
        decimal_places=2,
    )

    methods_used = models.ManyToManyField(
        PaymentMethod,
        related_name='users',
    )
    default_method = models.ForeignKey(
        PaymentMethod,
        related_name='users_by_default',
        null=True,
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
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def pay_item(self, item):
        """ Method for subtract cost of item.

        Raises:
            exceptions.ValidationError: User does not have enough money
        """
        if not self.can_pay(item.price):
            raise exceptions.ValidationError("Not enough money")

        # create new negative transaction
        PaymentTransaction(
            user=self,
            amount=-item.price,
        ).save()

    def can_pay(self, amount):
        """ Checking that user have 'amount' of money"""
        return self.balance >= amount

    def check_default_method(self):
        """ Checking that default method in methods_used """
        return self.methods_used.filter(pk=self.default_method.pk).exists()

    def update_balance(self):
        """ Method to recalculated user balance. """
        self.balance = PaymentTransaction.objects \
            .filter(user=self) \
            .aggregate(total_amount=Sum('amount')).get('total_amount')

        self.save(update_fields=['balance'])
        self.refresh_from_db()


class PaymentTransaction(TimeStampedModel, models.Model):
    """Model for storing operations with user balance """
    user = models.ForeignKey(AppUser)
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True)

    def save(self, **kwargs):
        super().save(**kwargs)
        # after creating a new transaction, the user balance will be updated
        self.user.update_balance()
