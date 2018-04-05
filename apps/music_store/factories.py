import factory
from factory import fuzzy

from .models import PaymentAccount, Track, PaymentMethod
from ..users.factories import UserFactory


class PaymentMethodFactory(factory.DjangoModelFactory):
    """Factory for generates test Payment methods."""

    class Meta:
        model = PaymentMethod


class PaymentAccountFactory(factory.DjangoModelFactory):
    """Factory for generates test Payment Account model with random AppUser

    Account balance is random from 0 to 1000.
    """
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = PaymentAccount

    @factory.lazy_attribute
    def balance(self):
        return fuzzy.FuzzyFloat(0, 1000).fuzz()


class TrackFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title """

    class Meta:
        model = Track

    @factory.lazy_attribute
    def price(self):
        return fuzzy.FuzzyFloat(0, 1000).fuzz()

    @factory.lazy_attribute
    def title(self):
        return fuzzy.FuzzyText().fuzz()
