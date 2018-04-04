from django.db import models


class MusicAlbum(models.Model):
    """Music album"""
    album_name = models.CharField(max_length=200)
    album_image = models.CharField(max_length=200)
    album_price = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.album_name


class MusicTrack(models.Model):
    """Music track"""
    track_name = models.CharField(max_length=200)
    track_album = models.ForeignKey(MusicAlbum, blank=True, null=True)
    track_price = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def set_like(self, user):
        """Method to put like on track"""
        pass

    def del_like(self, user):
        """Method to take away like from track"""
        pass

    def play_track(self, user):
        """Method to play music track"""
        pass

    def buy_track(self, user):
        """Method to buy music track"""
        pass

    def __str__(self):
        return self.track_name

