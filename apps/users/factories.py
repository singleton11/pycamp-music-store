import factory

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
