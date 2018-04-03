from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from faker import Faker

from ..factories import UserFactory
from ..views import UserUpdateView

fake = Faker()


class TestUserViews(TestCase):
    """Test for views of ``users`` app.

    Test updating user info with fake data, such as ``first name`` and
    ``last name``.

    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_update_user_access(self):
        """Test for access to update profile page.

        Not should be return code HTTP 200.

        """
        request = self.factory.get(reverse('users:profile'))
        request.user = AnonymousUser()
        response = UserUpdateView.as_view()(request)

        self.assertFalse(response.status_code is 200)

    def test_update_user(self):
        """Test for updating user profile.

        Checking for working UserUpdateView view.

        """
        first_name, last_name = fake.first_name(), fake.last_name()
        url = reverse('users:profile')
        data = {
            'first_name': first_name,
            'last_name': last_name
        }
        request = self.factory.post(url, data)
        request.user = self.user

        UserUpdateView.as_view()(request)

        self.assertEqual(
            (self.user.first_name, self.user.last_name),
            (first_name, last_name)
        )
