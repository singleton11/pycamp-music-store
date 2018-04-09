import factory
import factory.fuzzy

from .. import models


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Album

    title = factory.Faker('sentence', nb_words=2)
    image = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyFloat(0, 5.0)


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Track

    title = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyFloat(0, 5.0)
    album = factory.SubFactory(AlbumFactory)
