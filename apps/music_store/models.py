from django.contrib.auth import get_user_model
from django.db import models

AppUser = get_user_model()


class Track:
    """Blank model for Track"""
    pass


class Album:
    """Blank model for Album"""
    pass


class PaymentMethod(models.Model):
    """Model to store payment methods.

    User can select method Only admin can create methods.
    """
    title = models.CharField(max_length=100)


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

    payment_methods = models.ManyToManyField(PaymentMethod)
    default_payment_methods = models.ForeignKey(PaymentMethod)


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
