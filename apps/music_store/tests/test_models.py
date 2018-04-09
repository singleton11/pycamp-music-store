from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Album, Track, ListenTrack, LikeTrack
from ..tests.factories import AlbumFactory, TrackFactory
from ...users.factories import UserFactory


class TestAlbumAndTrack(TestCase):

    def setUp(self):
        self.album = AlbumFactory()
        self.track = TrackFactory()

    def test_album_str(self):
        self.assertEqual(str(self.album), self.album.title)

    def test_album_is_empty(self):
        album = Album(
            title='dersdbfcxbfd',
            image='sdrgdshgb//srgteawrtg/srge',
            price=199.99
        )
        self.assertTrue(album.is_empty)

    def test_track_str(self):
        self.assertEqual(str(self.track), self.track.title)

    def test_track_no_album(self):
        track = Track(
            title='vxdrgdfhbs',
            price=10.99
        )
        self.assertFalse(track.album)

    def test_track_has_album(self):
        self.assertTrue(self.track.album)

    def test_add_track_to_album(self):
        track = Track(
            title='vxdrgdfhbs',
            price=10.99,
            album=self.album,
        )
        self.assertEqual(track.album, self.album)


class TestLike(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.track = TrackFactory()
        self.like1 = LikeTrack(user=self.user1, track=self.track)
        self.like2 = LikeTrack(user=self.user2, track=self.track)
        self.like1.save()
        self.like2.save()

    def test_create_like(self):
        self.assertEqual(2, len(LikeTrack.objects.all()))

    def test_user_cannot_add_second_like(self):
        second_like = LikeTrack(user=self.user1, track=self.track)
        with self.assertRaises(IntegrityError):
            second_like.save()


class TestListen(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.track = TrackFactory()
        self.listen1 = ListenTrack(user=self.user1, track=self.track)
        self.listen2 = ListenTrack(user=self.user2, track=self.track)

        self.listen1.save()
        self.listen2.save()

    def test_create_listens(self):
        self.assertEqual(2, len(ListenTrack.objects.all()))

    def test_user_can_add_second_listen(self):
        second_listen = ListenTrack(user=self.user1, track=self.track)
        second_listen.save()
        self.assertEqual(2, len(ListenTrack.objects.filter(user=self.user1)))

        another_listen = ListenTrack(user=self.user2, track=self.track)
        another_listen.save()
        self.assertEqual(2, len(ListenTrack.objects.filter(user=self.user2)))
