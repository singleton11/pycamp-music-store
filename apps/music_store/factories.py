import factory
from factory import fuzzy

from apps.users.models import PaymentMethod
from .models import Track


class PaymentMethodFactory(factory.DjangoModelFactory):
    """ Factory to create payment method with random title """

    title = factory.Sequence(lambda n: "Method %03d" % n)

    class Meta:
        model = PaymentMethod


class TrackFactory(factory.DjangoModelFactory):
    """Factory for generates test Track model with random price and title """

    price = fuzzy.FuzzyFloat(0, 1000)
    title = fuzzy.FuzzyText()

    class Meta:
        model = Track
