import factory
from factory import fuzzy

from apps.users.factories import UserFactory
from .models import (
    Album,
    BoughtTrack,
    LikeTrack,
    ListenTrack,
    Track,
    PaymentTransaction,
    PaymentMethod,
    BoughtAlbum
)


class AlbumFactory(factory.django.DjangoModelFactory):
    author = factory.Faker('name')
    title = factory.Faker('sentence', nb_words=2)
    image = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)

    class Meta:
        model = Album


class TrackWithoutAlbumFactory(factory.django.DjangoModelFactory):
    """Track factory without album"""
    author = factory.Faker('name')
    title = factory.Faker('sentence', nb_words=2)
    price = factory.fuzzy.FuzzyInteger(0, 50)
    full_version = factory.Faker('sentence', nb_words=2)

    class Meta:
        model = Track


class TrackFactory(TrackWithoutAlbumFactory):
    """Track factory with album"""
    album = factory.SubFactory(AlbumFactory)


class TrackFactoryLongFullVersion(TrackFactory):
    """For tracks with long full_version text"""
    full_version = factory.Faker('sentence', nb_words=30)


class PaymentMethodFactory(factory.DjangoModelFactory):
    """Factory to create payment method with random title"""

    owner = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Method %03d" % n)
    is_default = False

    class Meta:
        model = PaymentMethod


class PaymentDefaultMethodFactory(PaymentMethodFactory):
    """Factory to create default payment method"""
    is_default = True


class PaymentTransactionFactory(factory.DjangoModelFactory):
    """Factory to create payment transaction for 'user' with 'amount'"""

    user = factory.SubFactory(UserFactory)
    amount = fuzzy.FuzzyInteger(1, 1000)
    payment_method = factory.SubFactory(PaymentMethodFactory)

    class Meta:
        model = PaymentTransaction


class UserWithPaymentMethodFactory(UserFactory):
    """Factory to create user with one payment method set by default"""

    payment_methods = factory.RelatedFactory(
        PaymentMethodFactory,
        'owner',
    )


class UserWithDefaultPaymentMethodFactory(UserFactory):
    """Factory to create user with one payment method"""

    payment_methods = factory.RelatedFactory(
        PaymentDefaultMethodFactory,
        'owner',
        is_default=True,
    )


class UserWithBalanceFactory(UserWithDefaultPaymentMethodFactory):
    """Factory to create AppUser with balance."""
    transactions = factory.RelatedFactory(
        PaymentTransactionFactory,
        'user',
        amount=factory.SelfAttribute('user.balance'),
        payment_method=factory.SelfAttribute('user.default_payment'),
    )


class BoughtTrackFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title"""

    item = factory.SubFactory(
        TrackFactory,
        price=fuzzy.FuzzyInteger(1, 10),
    )
    user = factory.SubFactory(
        UserWithPaymentMethodFactory,
        balance=fuzzy.FuzzyInteger(11, 20)
    )

    @factory.lazy_attribute
    def transaction(self):
        return PaymentTransactionFactory(user=self.user)

    class Meta:
        model = BoughtTrack


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


class BoughtAlbumFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title"""

    item = factory.SubFactory(
        AlbumFactory,
        price=fuzzy.FuzzyInteger(1, 10),
    )
    user = factory.SubFactory(
        UserWithPaymentMethodFactory
    )

    @factory.lazy_attribute
    def transaction(self):
        return PaymentTransactionFactory(user=self.user)

    class Meta:
        model = BoughtAlbum
