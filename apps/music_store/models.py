from django.contrib.auth import get_user_model
from django.db import models

AppUser = get_user_model()


class Track:
    pass


class Album:
    pass


class StoreUser(models.Model):
    user = models.OneToOneField(AppUser)
    balance = models.FloatField(default=0.0)


class BoughtTrack(models.Model):
    track = models.ForeignKey(Track)
    date_purchase = models.DateTimeField()
