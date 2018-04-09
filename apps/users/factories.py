import factory
from factory import fuzzy

from apps.users.models import PaymentTransaction, PaymentMethod
from .models import AppUser


class UserFactory(factory.DjangoModelFactory):
    """Factory for generates test User model.

    There are required fields first_name, last_name, username and email.

    """

    username = factory.Faker('user_name')

    class Meta:
        model = AppUser

    @factory.lazy_attribute
    def email(self):
        return "{0}@example.com".format(self.username)


class PaymentMethodFactory(factory.DjangoModelFactory):
    """ Factory to create payment method with random title """

    title = factory.Sequence(lambda n: "Method %03d" % n)

    class Meta:
        model = PaymentMethod


class PaymentTransactionFactory(factory.DjangoModelFactory):
    """ Factory to create payment transaction for 'user' with 'amount' """

    user = factory.SubFactory(UserFactory)
    amount = fuzzy.FuzzyInteger(1, 1000)

    class Meta:
        model = PaymentTransaction


class UserWithDefaultPaymentMethodFactory(UserFactory):
    """ Factory to create payment method with one payment_method """

    default_method = factory.SubFactory(PaymentMethodFactory)


class UserWithBalanceFactory(UserFactory):
    """ Factory to create User with balance. """
    transactions = factory.RelatedFactory(
        PaymentTransactionFactory,
        'user',
        amount=factory.SelfAttribute('user.balance')
    )


class UserWithAvatarFactory(UserFactory):
    """Custom factory for testing user with avatar.

    The factory creates really user avatar file.

    """
    avatar = factory.django.ImageField(color='magenta')


class AdminUserFactory(UserFactory):
    """Factory for generates test User model with admin's privileges """

    class Meta:
        model = AppUser

    is_superuser = True
    is_staff = True
