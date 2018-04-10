from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.music_store.factories import BoughtTrackFactory
from apps.music_store.models import Album, LikeTrack, ListenTrack, Track
from apps.users.factories import UserFactory, UserWithBalanceFactory, \
    PaymentMethodFactory
from ..factories import (
    TrackFactory,
)
from django.test import TestCase

from ..tests.factories import (
    AlbumFactory,
    TrackFactory,
    TrackFactoryLongFullVersion,
)


class TestPaymentAccount(TestCase):
    """Test for PaymentAccount and his methods

    This test is testing AppUser model.
    """

    def setUp(self):
        self.account = UserWithBalanceFactory(balance=100)
        self.count_methods = 5
        self.methods = [
            PaymentMethodFactory() for i in range(self.count_methods)
        ]

    def test_not_enough_money(self):
        track = TrackFactory(price=200)
        with self.assertRaises(ValidationError):
            self.account.pay_item(track)
        self.assertEqual(self.account.balance, 100)

    def test_save_negative_balance(self):
        with self.assertRaises(ValidationError):
            UserWithBalanceFactory(balance=-10)

    def test_enough_money(self):
        track = TrackFactory(price=10)
        self.account.pay_item(track)
        self.assertEqual(self.account.balance, 90)

    def test_select_methods(self):
        account = UserFactory()
        account.methods_used.add(*self.methods)
        account.default_method, *_ = self.methods
        account.save()
        self.assertEqual(account.methods_used.count(), self.count_methods)

    def test_set_default_methods(self):
        account = UserFactory()
        account.methods_used.add(PaymentMethodFactory())
        account.default_method = PaymentMethodFactory()
        self.assertFalse(account.check_default_method())


class TestBought(TestCase):
    """Test for buy tracks and albums and his methods

    This test is testing AppUser model.
    """

    def setUp(self):
        self.account = UserWithBalanceFactory(balance=100)
        self.count_tracks = 5
        self.tracks = TrackFactory.create_batch(self.count_tracks)

    def test_dublicate(self):
        track = self.tracks[0]
        BoughtTrackFactory(user=self.account, item=track)
        with self.assertRaises(IntegrityError):
            BoughtTrackFactory(user=self.account, item=track)

    def test_more_buy(self):
        for track in self.tracks:
            BoughtTrackFactory(user=self.account, item=track)
        count_bought = self.account.boughttrack_set.count()
        self.assertEqual(count_bought, self.count_tracks)


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
