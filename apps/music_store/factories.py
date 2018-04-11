import factory
from factory import fuzzy

from apps.music_store.models import BoughtAlbum
from apps.users.factories import UserWithBalanceFactory
from .models import Album, BoughtTrack, Track


class AlbumFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=2)
    image = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)

    class Meta:
        model = Album


class TrackFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)
    album = factory.SubFactory(AlbumFactory)
    full_version = factory.Faker('sentence', nb_words=2)

    class Meta:
        model = Track


class TrackFactoryLongFullVersion(TrackFactory):
    """For tracks with long full_version text

    """
    full_version = factory.Faker('sentence', nb_words=30)


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


class BoughtAlbumFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title """

    item = factory.SubFactory(
        AlbumFactory,
        price=fuzzy.FuzzyInteger(1, 10),
    )
    user = factory.SubFactory(
        UserWithBalanceFactory,
        balance=fuzzy.FuzzyInteger(11, 20)
    )

    class Meta:
        model = BoughtAlbum
