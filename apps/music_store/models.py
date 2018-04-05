from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

AppUser = get_user_model()


class Track(models.Model):
    """ part of model for Track"""
    track_name = models.CharField(max_length=200, default="Undefined")
    track_price = models.FloatField(default=1.0)

    def __str__(self):
        return self.track_name


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
    user = models.OneToOneField(AppUser, primary_key=True)
    balance = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )

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

    def pay_track(self, track):
        # ToDo: save to history
        # ToDo: block the table
        if self.balance < track.track_price:
            return False
        self.balance -= track.track_price
        self.save()
        return True


class BoughtTrack(models.Model):
    """Model for storing a bought track after purchase

    Attributes:
        user(AppUser): user who bought the track
        track(AppUser): track purchased by the user
        date_purchase(DateTimeField): date of purchase
    """
    user = models.ForeignKey(AppUser)
    track = models.ForeignKey(Track)
    date_purchase = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "track"),)

    def __str__(self):
        return f'{self.user} bought {self.track}'
