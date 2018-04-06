from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.factories import UserFactory, UserWithBalanceFactory
from ..factories import (
    TrackFactory,
    PaymentMethodFactory,
)


class TestPaymentAccount(TestCase):
    """Test for PaymentAccount and his methods

    This test is testing AppUser model.
    """

    def setUp(self):
        self.account = UserWithBalanceFactory(balance=100)

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
        count = 5
        methods = [PaymentMethodFactory() for i in range(count)]
        account.methods_used.add(*methods)
        account.default_method = methods[1]
        account.save()
        self.assertEqual(len(account.methods_used.all()), count)

    def test_set_default_methods(self):
        account = UserFactory()
        account.methods_used.add(PaymentMethodFactory())
        account.default_method = PaymentMethodFactory()
        self.assertFalse(account.check_default_method())
