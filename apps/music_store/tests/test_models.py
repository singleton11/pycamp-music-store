from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

import factory

from apps.music_store.factories import (
    AlbumFactory,
    BoughtAlbumFactory,
    BoughtTrackFactory,
    LikeTrackFactory,
    ListenTrackFactory,
    TrackFactory,
    TrackFactoryLongFullVersion,
    UserWithBalanceFactory,
    PaymentMethodFactory,
    PaymentDefaultMethodFactory,
    UserWithDefaultPaymentMethodFactory,
    UserWithPaymentMethodFactory
)
from apps.music_store.models import Album, LikeTrack, ListenTrack, Track
from apps.users.factories import UserFactory


class TestPaymentAccount(TestCase):
    """Test for PaymentAccount and his methods

    This test is testing AppUser model.
    """

    def setUp(self):
        self.account = UserWithBalanceFactory(balance=100)
        self.count_methods = 5
        self.methods = PaymentMethodFactory.create_batch(self.count_methods)

    def test_not_enough_money(self):
        track = TrackFactory(price=200)
        with self.assertRaises(ValidationError):
            track.buy(self.account)
        self.assertEqual(self.account.balance, 100)

    def test_save_negative_balance(self):
        with self.assertRaises(ValidationError):
            UserWithBalanceFactory(balance=-10)

    def test_enough_money(self):
        track = TrackFactory(price=10)
        track.buy(self.account)
        self.assertEqual(self.account.balance, 90)

    def test_select_methods(self):
        account = UserWithPaymentMethodFactory()
        self.assertEqual(account.payment_methods.count(), 1)

    def test_set_default_method(self):
        account = UserWithDefaultPaymentMethodFactory()
        self.assertEqual(account.payment_methods.count(), 1)
        self.assertTrue(account.payment_methods.first().is_default)

    def test_set_new_default_method(self):
        account = UserWithDefaultPaymentMethodFactory()
        PaymentDefaultMethodFactory(owner=account)
        PaymentDefaultMethodFactory(owner=account)

        self.assertEqual(account.payment_methods.count(), 3)
        self.assertEqual(
            account.payment_methods.filter(is_default=True).count(),
            1,
        )


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
        cls.user = UserFactory()
        cls.album = AlbumFactory()
        cls.track = TrackFactory()
        cls.long_track = TrackFactoryLongFullVersion()

    def test_album_str(self):
        self.assertEqual(
            str(self.album),
            f'{self.album.author} - {self.album.title}'
        )

    def test_album_is_empty(self):
        album = Album(
            title='dersdbfcxbfd',
            image='sdrgdshgb srgteawrtg srge',
            price=19999
        )
        self.assertTrue(album.is_empty)

    def test_album_is_not_bought(self):
        self.assertFalse(self.album.is_bought(self.user))

    def test_album_is_bought(self):
        BoughtAlbumFactory(item=self.album, user=self.user)
        self.assertTrue(self.album.is_bought(self.user))

    def test_track_str(self):
        self.assertEqual(
            str(self.track),
            f'{self.track.author} - {self.track.title}'
        )

    def test_add_track_to_album(self):
        track = Track(
            title='vxdrgdfhbs',
            price=10,
            album=self.album,
        )
        self.assertEqual(track.album, self.album)

    def test_track_is_not_bought(self):
        self.assertFalse(self.track.is_bought(self.user))

    def test_track_is_bought(self):
        BoughtTrackFactory(item=self.track, user=self.user)
        self.assertTrue(self.track.is_bought(self.user))

    def test_track_is_not_liked(self):
        self.assertFalse(self.track.is_liked(self.user))

    def test_track_is_liked(self):
        LikeTrackFactory(track=self.track, user=self.user)
        self.assertTrue(self.track.is_liked(self.user))

    def test_free_version_of_track_equal_to_short_full_version(self):
        self.assertEqual(self.track.free_version, self.track.full_version)

    def test_free_version_of_track_not_equal_to_long_full_version(self):
        self.assertNotEqual(
            self.long_track.free_version,
            self.long_track.full_version
        )

        self.assertEqual(
            self.long_track.free_version,
            self.long_track.full_version[:25]
        )

    def test_like_track(self):
        self.track.like(user=self.user)
        self.assertTrue(self.track.is_liked(user=self.user))

    def test_cannot_like_track_multiple_times(self):
        likes = 3
        for i in range(likes):
            self.track.like(user=self.user)
        self.assertEqual(
            1,
            LikeTrack.objects.filter(user=self.user, track=self.track).count()
        )

    def test_unlike_track(self):
        LikeTrackFactory(user=self.user, track=self.track)
        self.track.unlike(user=self.user)
        self.assertFalse(self.track.is_liked(user=self.user))

    def test_listen_to_track(self):
        self.track.listen(user=self.user)
        self.assertTrue(
            ListenTrack.objects.filter(user=self.user,
                                       track=self.track).exists()
        )

    def test_listen_multiple_times(self):
        listens = 3
        for i in range(listens):
            self.track.listen(user=self.user)
        self.assertEqual(
            listens,
            ListenTrack.objects.filter(user=self.user,
                                       track=self.track).count()
        )


class TestLike(TestCase):

    def test_create_likes(self):
        count = 2
        users = UserFactory.create_batch(count)
        track = TrackFactory()
        LikeTrackFactory.create_batch(
            count,
            user=factory.Iterator(users),
            track=track
        )

        self.assertEqual(count, LikeTrack.objects.count())


class TestListen(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.count = 3
        cls.users = UserFactory.create_batch(cls.count)
        cls.track = TrackFactory()
        cls.listens = ListenTrackFactory.create_batch(
            cls.count,
            user=factory.Iterator(cls.users),
            track=cls.track
        )

    def test_create_listens(self):
        self.assertEqual(self.count, ListenTrack.objects.count())

    def test_listen_track_many_times(self):
        repeat_listens = 3
        repeat_user = UserFactory()
        for i in range(repeat_listens):
            ListenTrackFactory(user=repeat_user, track=self.track)

        self.assertEqual(
            ListenTrack.objects.filter(user=repeat_user).count(),
            repeat_listens
        )
