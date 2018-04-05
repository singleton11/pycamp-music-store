from django.test import TestCase

from ..models import Album, Track


class TestAlbumAndTrack(TestCase):
    """"""

    def setUp(self):
        self.album = Album(
            title='dersdbfcxbfd',
            image='sdrgdshgb//srgteawrtg/srge',
            price=199.99
        )
        self.track = Track(
            title='vxdrgdfhbs',
            price=10.99
        )

    def test_album_str(self):
        self.assertEqual(str(self.album), self.album.title)

    def test_album_is_empty(self):
        self.assertTrue(self.album.is_empty)

    def test_track_str(self):
        self.assertEqual(str(self.track), self.track.title)

    def test_track_no_album(self):
        self.assertFalse(self.track.album)

    def test_add_track_to_album(self):
        self.track.album = self.album
        self.assertEqual(self.track.album, self.album)
