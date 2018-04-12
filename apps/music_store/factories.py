import factory
from factory import fuzzy

from apps.users.factories import UserFactory
from .models import Album, BoughtTrack, Track, PaymentTransaction, \
    PaymentMethod


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
    """For tracks with long full_version text """
    full_version = factory.Faker('sentence', nb_words=30)


class PaymentMethodFactory(factory.DjangoModelFactory):
    """ Factory to create payment method with random title """

    owner = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Method %03d" % n)
    is_default = False

    class Meta:
        model = PaymentMethod


class PaymentDefaultMethodFactory(PaymentMethodFactory):
    """ Factory to create default payment method"""
    is_default = True


class PaymentTransactionFactory(factory.DjangoModelFactory):
    """ Factory to create payment transaction for 'user' with 'amount' """

    user = factory.SubFactory(UserFactory)
    amount = fuzzy.FuzzyInteger(1, 1000)

    class Meta:
        model = PaymentTransaction


class UserWithPaymentMethodFactory(UserFactory):
    """ Factory to create user with one payment method set by dafault """

    payment_methods = factory.RelatedFactory(
        PaymentMethodFactory,
        'owner',
    )


class UserWithDefaultPaymentMethodFactory(UserFactory):
    """ Factory to create user with one payment method """

    payment_methods = factory.RelatedFactory(
        PaymentDefaultMethodFactory,
        'owner',
        is_default=True,
    )


class UserWithBalanceFactory(UserWithDefaultPaymentMethodFactory):
    """ Factory to create AppUser with balance. """
    transactions = factory.RelatedFactory(
        PaymentTransactionFactory,
        'user',
        amount=factory.SelfAttribute('user.balance')
    )


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
    transaction = factory.SubFactory(
        PaymentTransactionFactory,
        user=user
    )

    class Meta:
        model = BoughtTrack
