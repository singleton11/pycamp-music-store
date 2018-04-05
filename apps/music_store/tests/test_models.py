from django.test import TestCase

from apps.users.factories import UserFactory
from ..factories import (
    TrackFactory,
    PaymentMethodFactory,
)


class TestPaymentAccount(TestCase):
    """Test for PaymentAccount and his methods

    This test is testing AppUser model.
    """

    def setUp(self):
        self.account = UserFactory(balance=100)

    def test_save_negative_balance_1(self):
        self.account.balance = -1
        with self.assertRaises(ValueError):
            self.account.save()

    def test_save_negative_balance_2(self):
        with self.assertRaises(ValueError):
            UserFactory(balance=-10)

    def test_not_enough_money(self):
        track = TrackFactory(price=200)
        result = self.account.pay_item(track)
        self.assertEqual(result, False)
        self.assertEqual(self.account.balance, 100)

    def test_enough_money(self):
        track = TrackFactory(price=10)
        result = self.account.pay_item(track)
        self.assertEqual(result, True)
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
        self.assertEqual(account.check_default_method(), False)
