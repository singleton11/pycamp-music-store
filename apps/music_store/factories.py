import factory
from factory import fuzzy

from apps.users.factories import UserWithBalanceFactory
from .models import Track, BoughtTrack


class TrackFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title """

    price = fuzzy.FuzzyFloat(0, 1000)
    title = fuzzy.FuzzyText()

    class Meta:
        model = Track


class BoughtTrackFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title """

    item = factory.SubFactory(
        TrackFactory,
        price=fuzzy.FuzzyInteger(1, 10),
    )
    user = factory.SubFactory(
        UserWithBalanceFactory,
        balance=fuzzy.FuzzyInteger(11, 20)
    )

    class Meta:
        model = BoughtTrack
