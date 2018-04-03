import tempfile
import unittest
from operator import methodcaller

from django.test import override_settings

from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from faker import Faker
from PIL import Image

from ..api.views import (
    CheckUsernameView,
    UserGeoLocationAPIView,
    UserUploadAvatarAPIView,
)
from ..factories import UserFactory

fake = Faker()


@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class TestAPIUser(APITestCase):
    """Test for API of ``users`` app.

    Contains tests for upload avatar, location view and user exists.

    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = UserFactory()

    def _get_response_for_avatar_api(self, url, method, data=None):
        call_method = methodcaller(method, url, data)
        request = call_method(self.factory)

        force_authenticate(request, user=self.user)

        return UserUploadAvatarAPIView.as_view()(request)

    def _get_response_for_username_api(self, url, username):
        request = self.factory.get(url.format(username=username))

        force_authenticate(request, user=self.user)

        return CheckUsernameView.as_view()(request, username=username)

    def _get_responce_for_location_api(self, data):
        url = '/api/v1/auth/user/location/'
        request = self.factory.post(url, data)

        force_authenticate(request, user=self.user)

        return UserGeoLocationAPIView.as_view()(request)

    def _get_response_for_password_api(self, data):
        url = '/api/v1/auth/password/reset/'

        self.client.force_authenticate(user=self.user)

        return self.client.post(url, data, format='json')

    @unittest.skip("FIX")
    def test_avatar_api(self):
        """Test for avatar API.

        Test for upload, get url and delete for uploaded avatar.

        """
        url = '/api/v1/user/avatar/'
        image = Image.new('RGB', (500, 500), 'green')
        tmp_file = tempfile.NamedTemporaryFile()

        image.save(tmp_file.name, 'PNG')

        # request contains `upload`
        data = {'upload': tmp_file}
        response = self._get_response_for_avatar_api(url, 'post', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # request does not contain `upload`
        response = self._get_response_for_avatar_api(url, 'post')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # delete the uploaded avatar
        response = self._get_response_for_avatar_api(url, 'delete')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # delete if avatar does not exist
        self.user.avatar = None
        response = self._get_response_for_avatar_api(url, 'delete')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skip("FIX")
    def test_username_api(self):
        """Test for username existance.

        Raise http 404 if username already registered and 200 if does not.

        """
        url = '/api/v1/auth/check/{username}/'

        # if username exists
        username = self.user.username
        response = self._get_response_for_username_api(url, username)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # if username does not exists
        username = fake.user_name()
        response = self._get_response_for_username_api(url, username)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_location_create_api(self):
        """Test for Geo location API view.

        The view should be change coordinates of the user and return HTTP 200.

        """
        data = {
            'lat': fake.latitude(),
            'lon': fake.longitude()
        }
        response = self._get_responce_for_location_api(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_location_create_api(self):
        """Test for Geo location API view vith invalid data.

        The view should be get HTTP 400 Bad request. Provide not valid key
        `long` (instead valid `lon`) in `data`.

        """
        data = {
            'lat': fake.latitude(),
            'long': fake.longitude()
        }
        response = self._get_responce_for_location_api(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_api(self):
        """Test for password reset.

        Should be returns HTTP 200 OK if user with the email exists.

        """
        data = {
            'email': self.user.email
        }
        response = self._get_response_for_password_api(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_invalid_reset_api(self):
        """Test for password reset with invalid data.

        Should be returns HTTP 400 Bad request. Provide fake email of
        unexisting user.

        """
        data = {
            'email': fake.email()
        }
        response = self._get_response_for_password_api(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_api(self):
        """Test for create new user API.

        Should be returns HTTP 201 Created if user has been created
        successfully.

        """
        url = '/api/v1/auth/register'
        password = fake.password()
        data = {
            'password1': password,
            'password2': password,
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name()
        }

        self.client.force_authenticate(user=None)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
