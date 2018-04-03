import os

from django.test import TestCase

from ..factories import UserWithAvatarFactory
from ..models import AppUser


class TestUser(TestCase):
    """Test for create a User.

    This test is testing AppUser model.

    """

    def setUp(self):
        self.user = UserWithAvatarFactory()

    def test_exists_avatar(self):
        """Test for the user`s avatar file.

        First assert checks for file existance, second -- for file removes.

        """
        path = self.user.avatar.path

        self.assertFalse(not os.path.isfile(path))

        try:
            os.remove(path)
            removed = True
        except:
            removed = False

        self.assertFalse(not removed)

    def test_str_returns_username(self):
        """Test for correct object representation for __str__.

        User object should be return ``username``.

        """
        self.assertEqual(self.user.__str__(), self.user.username)

    def test_create_user(self):
        """Test for user model.

        Checking for existance the created user.

        """
        user = AppUser.objects.filter(email=self.user.email)

        self.assertEqual(user.exists(), True)
