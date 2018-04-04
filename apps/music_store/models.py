from django.contrib.auth import get_user_model
from django.db import models

AppUser = get_user_model()


class Track(models.Model):
    """Blank model for Track"""
    pass


class Album(models.Model):
    """Blank model for Album"""
    pass


class PaymentMethod(models.Model):
    """Model to store payment methods.

    User can select method Only admin can create methods.
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PaymentAccount(models.Model):
    """Payment account for each user

    Attributes:
        user(AppUser): owner of this payment account.
        balance(float): current balance.
        payment_methods(PaymentMethod[]): saved payment methods
        default_payment_methods(PaymentMethod): default payment method
    """
    user = models.OneToOneField(AppUser)
    balance = models.FloatField(default=0.0)

    methods_used = models.ManyToManyField(
        PaymentMethod,
        related_name='methods_used'
    )
    default_method = models.ForeignKey(
        PaymentMethod,
        related_name='default_method'
    )

    def __str__(self):
        return f'{self.user} (balance {self.balance})'


class BoughtTrack(models.Model):
    """Model for storing a bought track after purchase

    Attributes:
        user(AppUser): user who bought the track
        track(AppUser): track purchased by the user
        date_purchase(DateTimeField): date of purchase
    """
    user = models.ForeignKey(AppUser)
    track = models.ForeignKey(Track)
    date_purchase = models.DateTimeField()

    class Meta:
        unique_together = (("user", "track"),)

    def __str__(self):
        return f'{self.user} bought {self.track}'
