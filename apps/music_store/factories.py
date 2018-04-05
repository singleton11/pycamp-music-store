import factory
from factory import fuzzy

from apps.users.models import PaymentMethod
from .models import Track


class PaymentMethodFactory(factory.DjangoModelFactory):
    """Factory for generates test Payment methods."""

    class Meta:
        model = PaymentMethod


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
