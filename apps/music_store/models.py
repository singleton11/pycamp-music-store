from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

AppUser = get_user_model()


class Track(models.Model):
    """ part of model for Track"""
    title = models.CharField(max_length=200, default="Undefined")
    price = models.FloatField(default=1.0)

    def __str__(self):
        return self.title


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
        related_name='methods_used',
    )
    default_method = models.ForeignKey(
        PaymentMethod,
        related_name='default_method',
        null=True,
    )

    def __str__(self):
        return f'{self.user} (balance {self.balance})'

    def pay_item(self, item):
        """ Method for subtract cost of item.

        Returns:
            boolean: True, if success
        """
        # ToDo: save to history
        # ToDo: block the table
        if self.balance < item.price:
            return False
        self.balance -= item.price
        self.save()
        return True

    def check_default_method(self):
        """ Check, that default method in methods_used """
        return self.methods_used.filter(pk=self.default_method.pk).exists()

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValueError("Balance must be positive")
        super().save(*args, **kwargs)


class BoughtTrack(models.Model):
    """Model for storing a bought track after purchase

    Attributes:
        user(AppUser): user who bought the track
        track(Track): track purchased by the user
        date_purchase(DateTimeField): date of purchase
    """
    user = models.ForeignKey(AppUser)
    track = models.ForeignKey(Track)
    date_purchase = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "track"),)

    def __str__(self):
        return f'{self.user} bought {self.track}'


class BoughtAlbum(models.Model):
    """Model for storing a bought albums after purchase

    Attributes:
        user(AppUser): user who bought the album
        album(Album): album purchased by the user
        date_purchase(DateTimeField): date of purchase
    """
    user = models.ForeignKey(AppUser)
    album = models.ForeignKey(Album)
    date_purchase = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "album"),)

    def __str__(self):
        return f'{self.user} bought {self.album}'
