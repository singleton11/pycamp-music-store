from django.test import TestCase

from ...users.factories import UserFactory
from ..models import Album, LikeTrack, ListenTrack, Track
from ..tests.factories import (
    AlbumFactory,
    TrackFactory,
    TrackFactoryLongFullVersion,
)


class TestAlbumAndTrack(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.album = AlbumFactory()
        cls.track = TrackFactory()
        cls.long_track = TrackFactoryLongFullVersion()

    def test_album_str(self):
        self.assertEqual(str(self.album), self.album.title)

    def test_album_is_empty(self):
        album = Album(
            title='dersdbfcxbfd',
            image='sdrgdshgb srgteawrtg srge',
            price=19999
        )
        self.assertTrue(album.is_empty)

    def test_track_str(self):
        self.assertEqual(str(self.track), self.track.title)

    def test_add_track_to_album(self):
        track = Track(
            title='vxdrgdfhbs',
            price=10,
            album=self.album,
        )
        self.assertEqual(track.album, self.album)

    def test_free_version_equal_to_short_full_version(self):
        self.assertEqual(self.track.free_version, self.track.full_version)

    def test_free_version_not_equal_to_long_full_version(self):
        self.assertNotEqual(
            self.long_track.free_version,
            self.long_track.full_version
        )

        self.assertEqual(
            self.long_track.free_version,
            self.long_track.full_version[:25]
        )


class TestLike(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.track = TrackFactory()
        cls.like1 = LikeTrack(user=cls.user1, track=cls.track)
        cls.like2 = LikeTrack(user=cls.user2, track=cls.track)
        cls.like1.save()
        cls.like2.save()

    def test_create_like(self):
        self.assertEqual(2, LikeTrack.objects.count())


class TestListen(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.track = TrackFactory()
        cls.listen1 = ListenTrack(user=cls.user1, track=cls.track)
        cls.listen2 = ListenTrack(user=cls.user2, track=cls.track)
        cls.listen3 = ListenTrack(user=cls.user2, track=cls.track)

        cls.listen1.save()
        cls.listen2.save()
        cls.listen3.save()

    def test_create_listens(self):
        self.assertEqual(3, ListenTrack.objects.count())
