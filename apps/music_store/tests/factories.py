import factory
import factory.fuzzy

from .. import models


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Album

    title = factory.fuzzy.FuzzyText(length=12).fuzz()
    image = factory.fuzzy.FuzzyText(length=30).fuzz()
    price = factory.fuzzy.FuzzyFloat(0, 5.0).fuzz()


class TrackFactoryNoAlbum(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Track

    title = factory.fuzzy.FuzzyText(length=10).fuzz()
    # album = factory.SubFactory(AlbumFactory)
    price = factory.fuzzy.FuzzyFloat(0, 5.0).fuzz()
