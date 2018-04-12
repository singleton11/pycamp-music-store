import factory
from factory import fuzzy

from apps.users.factories import UserFactory, UserWithBalanceFactory

from .models import (
    Album,
    BoughtAlbum,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
)


class AlbumFactory(factory.django.DjangoModelFactory):

    author = factory.Faker('name')
    title = factory.Faker('sentence', nb_words=2)
    image = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)

    class Meta:
        model = Album


class TrackFactory(factory.django.DjangoModelFactory):

    author = factory.Faker('name')
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
    """Factory for generates test Album model with random price and title """

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


class LikeTrackFactory(factory.DjangoModelFactory):
    """Factory for ListenTrack instances"""

    track = factory.SubFactory(TrackFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LikeTrack


class ListenTrackFactory(factory.DjangoModelFactory):
    """Factory for ListenTrack instances"""

    track = factory.SubFactory(TrackFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = ListenTrack
