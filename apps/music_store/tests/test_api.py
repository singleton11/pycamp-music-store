from operator import methodcaller

from django.test import override_settings
from faker import Faker
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from apps.music_store.factories import TrackFactory, BoughtTrackFactory, \
    BoughtAlbumFactory, AlbumFactory
from apps.users.factories import UserWithBalanceFactory

fake = Faker()


@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class TestAPIMusicStoreBoughtItems(APITestCase):
    """Test for API of ``music_store`` app. """

    def _url(self, sub_url):
        return '/api/v1/music_store/' + sub_url

    def _api_bougth_track(self, data, user=None, method="post"):
        if user:
            self.client.force_authenticate(user=self.user)

        url = self._url('bought_tracks/')
        caller = methodcaller(method, url, data)
        return caller(self.client)

    def _api_bougth_album(self, data, user=None, method="post"):
        if user:
            self.client.force_authenticate(user=self.user)

        url = self._url('bought_albums/')
        caller = methodcaller(method, url, data)
        return caller(self.client)

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithBalanceFactory(balance=100)

        self.track = TrackFactory(price=10)
        self.track_high_price = TrackFactory(price=1000)

        self.album = AlbumFactory(price=10)
        self.album_high_price = AlbumFactory(price=1000)

    ##############################################################
    # Tests bought track
    ##############################################################

    def test_bought_track_empty_list(self):
        response = self._api_bougth_track(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bought_track_not_auth_get(self):
        response = self._api_bougth_track(data=None, user=None, method='get')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bought_track_buy_result_code(self):
        data = {'item': self.track.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_bought_track_buy_sub_balance(self):
        balance_before = self.user.balance

        data = {'item': self.track.pk}
        self._api_bougth_track(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.track.price)

    def test_bought_track_buy_not_enough_money(self):
        data = {'item': self.track_high_price.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bought_already_exists_track(self):
        BoughtTrackFactory(user=self.user, item=self.track)

        data = {'item': self.track.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    ##############################################################
    # Tests bought albums
    ##############################################################

    def test_bought_album_empty_list(self):
        response = self._api_bougth_album(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bought_album_not_auth_get(self):
        response = self._api_bougth_album(data=None, user=None, method='get')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bought_album_buy_result_code(self):
        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_bought_album_buy_sub_balance(self):
        balance_before = self.user.balance

        data = {'item': self.album.pk}
        self._api_bougth_album(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.album.price)

    def test_bought_album_buy_not_enough_money(self):
        data = {'item': self.album_high_price.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bought_already_exists_album(self):
        BoughtAlbumFactory(user=self.user, item=self.album)

        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
