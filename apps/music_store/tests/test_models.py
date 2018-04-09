from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.music_store.factories import BoughtTrackFactory
from apps.music_store.models import BoughtTrack
from apps.users.factories import UserFactory, UserWithBalanceFactory, \
    PaymentMethodFactory
from ..factories import (
    TrackFactory,
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
