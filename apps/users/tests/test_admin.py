import factory

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone
from django.utils.html import format_html

from faker import Faker

from ..admin import AppUserAdmin
from ..factories import UserWithAvatarFactory
from ..models import AppUser

faker = Faker()

@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class TestUserAdmin(TestCase):
    """Test for Admin of ``users`` app.

    Contains tests for base Admin class for ``users``.

    """

    def setUp(self):
        self.request = RequestFactory()
        self.site = AdminSite()
        self.ma = AppUserAdmin(AppUser, self.site)
        self.user = UserWithAvatarFactory(is_superuser=True)
        self.user.location.coords = (faker.longitude(), faker.latitude())
        self.user.location_updated = timezone.now()
        self.request.user = self.user

    def test_custom_fields_exist(self):
        """Test for existance some custom fields in Admin.

        This custom fields are `_avatar`, `_location` and `_location_updated`.

        """
        fields = self.ma.get_fields(self.request)
        expected_fields = ['_avatar', '_location', '_location_updated']

        self.assertEqual(
            len(expected_fields),
            len(set(expected_fields) & set(fields))
        )

    def test_avatar_exists(self):
        """Test for existence user avatar.

        Checking for returned an HTML `img` tag, that contains URL to avatar.

        """
        expected_html = "<img src='{0}' >".format(self.user.avatar.url)

        self.assertEqual(self.ma._avatar(self.user), expected_html)

    def test_avatar_does_not_exist(self):
        """Test for non existence user avatar.

        Should be returned string 'None'.

        """
        self.user.avatar = None

        self.assertEqual(self.ma._avatar(self.user), 'None')

    def test_location(self):
        """Test for returns location coordinates.

        Should be returned an HTML `a` tag, that contains a link to the point
        on Google Maps service.
        
        """
        coords = list(reversed(self.user.location.coords))
        url = 'http://maps.google.com/maps?t=h&q=loc:{0},{1},10z'.format(
            *coords
        )
        expected_link = format_html("<a href='{0}'>{1}, {2}</a>", url, *coords)

        self.assertEqual(self.ma._location(self.user), expected_link)

    def test_location_updated(self):
        """Test for returns location updated.

        Shold be returned a `datetime` object.

        """
        updated = self.ma._location_updated(self.user)

        self.assertFalse(not isinstance(updated, timezone.datetime))
