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

    owner = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Method %03d" % n)
    is_default = False

    class Meta:
        model = PaymentMethod


class PaymentDefaultMethodFactory(PaymentMethodFactory):
    """ Factory to create payment method with random title """
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
