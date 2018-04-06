from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Track(TitleDescriptionModel, models.Model):
    """ part of model for Track"""
    price = models.FloatField(default=1.0)

    def __str__(self):
        return self.title


class Album(models.Model):
    """ part of model for Album"""
    pass


AppUser = get_user_model()


class BoughtItem(TimeStampedModel, models.Model):
    """ An abstract base class model for BoughtTrack and BoughtAlbum
    """
    user = models.ForeignKey(AppUser)

    class Meta:
        abstract = True
        unique_together = (("user", "item"),)

    def __str__(self):
        return f'{self.user} bought {self.item}'


class BoughtTrack(BoughtItem, models.Model):
    """Model for storing a bought track after purchase

    Attributes:
        item(Track): track purchased by the user
    """
    item = models.ForeignKey(Track, verbose_name='track')


class BoughtAlbum(BoughtItem, models.Model):
    """Model for storing a bought albums after purchase

    Attributes:
        item(Album): album purchased by the user
    """
    item = models.ForeignKey(Album, verbose_name='album')
