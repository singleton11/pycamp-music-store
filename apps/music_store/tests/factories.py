import factory
import factory.fuzzy

from .. import models


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Album

    title = factory.Faker('sentence', nb_words=2)
    image = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Track

    title = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)
    album = factory.SubFactory(AlbumFactory)
    full_version = factory.Faker('sentence', nb_words=3)


class TrackFactoryLongFullVersion(TrackFactory):
    """For tracks with long full_version text
    """

    full_version = factory.Faker('sentence', nb_words=30)
