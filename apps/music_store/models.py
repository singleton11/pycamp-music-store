from django.contrib.auth import get_user_model
from django.db import models


class Track(models.Model):
    """ part of model for Track"""
    title = models.CharField(max_length=200, default="Undefined")
    price = models.FloatField(default=1.0)

    def __str__(self):
        return self.title

    def user_has(self, user):
        return BoughtTrack.objects.filter(user=user, track=self).exists()


class Album(models.Model):
    """Blank model for Album"""

    def user_has(self, user):
        return BoughtAlbum.objects.filter(user=user, album=self).exists()


AppUser = get_user_model()


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
