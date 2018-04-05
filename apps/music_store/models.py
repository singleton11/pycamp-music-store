from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Track(TitleDescriptionModel, models.Model):
    """ part of model for Track"""
    price = models.FloatField(default=1.0)

    def __str__(self):
        return self.title

    def user_has(self, user):
        return BoughtTrack.objects.filter(user=user, item=self).exists()


class Album(models.Model):
    def user_has(self, user):
        return BoughtAlbum.objects.filter(user=user, item=self).exists()


class BoughtItem(TimeStampedModel, models.Model):
    """ An abstract base class model for BoughtTrack and BoughtAlbum
    """
    user = models.ForeignKey(AUTH_USER_MODEL)

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
    item = models.ForeignKey(Track)


class BoughtAlbum(BoughtItem, models.Model):
    """Model for storing a bought albums after purchase

    Attributes:
        item(Album): album purchased by the user
    """
    item = models.ForeignKey(Album)
