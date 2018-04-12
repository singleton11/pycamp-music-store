from operator import methodcaller

from faker import Faker
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from apps.music_store.factories import (
    TrackFactory,
    BoughtTrackFactory,
    BoughtAlbumFactory,
    AlbumFactory,
)
from apps.users.factories import UserWithBalanceFactory

fake = Faker()


def api_url(relative_url):
    return '/api/v1/music_store/' + relative_url


class TestAPIMusicStoreBoughtTrack(APITestCase):
    """Test for API of ``music_store`` app for bought track. """

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithBalanceFactory(balance=100)

        self.track = TrackFactory(price=10)
        self.track_high_price = TrackFactory(price=1000)

    def test_bought_track_empty_list(self):
        """ Checking the display of an empty track list"""
        response = self._api_bougth_track(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_bought_track_list(self):
        """ Checking that the user sees only their purchased tracks"""
        BoughtTrackFactory()
        BoughtTrackFactory(user=self.user, item=self.track)
        BoughtTrackFactory(user=self.user, item=self.track_high_price)

        response = self._api_bougth_track(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_bought_track_not_auth_get(self):
        """ Unauthorized user verification"""
        response = self._api_bougth_track(data=None, user=None, method='get')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bought_track_buy_result_code(self):
        """ Checking the purchase result code"""
        data = {'item': self.track.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_bought_track_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance

        data = {'item': self.track.pk}
        self._api_bougth_track(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.track.price)

    def test_bought_track_buy_not_enough_money(self):
        """ Trying to buy a track for which there is not enough money"""
        data = {'item': self.track_high_price.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bought_already_exists_track(self):
        """ Trying to buy an already purchased track"""
        BoughtTrackFactory(user=self.user, item=self.track)

        data = {'item': self.track.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _api_bougth_track(self, data, user=None, method="post"):
        """ Method for send request to BoughtTrack Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url('bought_tracks/')
        caller = methodcaller(method, url, data)
        return caller(self.client)


class TestAPIMusicStoreBoughtAlbum(APITestCase):
    """Test for API of ``music_store`` app for bought album."""

    def _api_bougth_album(self, data, user=None, method="post"):
        """ Method for send request to BoughtAlbum Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url('bought_albums/')
        caller = methodcaller(method, url, data)
        return caller(self.client)

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithBalanceFactory(balance=100)

        self.album = AlbumFactory(price=10)
        self.album_high_price = AlbumFactory(price=1000)

    def test_bought_album_empty_list(self):
        """ Checking the display of an empty album list"""
        response = self._api_bougth_album(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_bought_album_list(self):
        """ Checking that the user sees only their purchased albums"""
        BoughtAlbumFactory()
        BoughtAlbumFactory(user=self.user, item=self.album)
        BoughtAlbumFactory(user=self.user, item=self.album_high_price)

        response = self._api_bougth_album(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_bought_album_not_auth_get(self):
        """ Unauthorized user verification"""
        response = self._api_bougth_album(data=None, user=None, method='get')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bought_album_buy_result_code(self):
        """ Checking the purchase result code"""
        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_bought_album_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance

        data = {'item': self.album.pk}
        self._api_bougth_album(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.album.price)

    def test_bought_album_buy_not_enough_money(self):
        """ Trying to buy a album for which there is not enough money"""
        data = {'item': self.album_high_price.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bought_already_exists_album(self):
        """ Trying to buy an already purchased album"""
        BoughtAlbumFactory(user=self.user, item=self.album)

        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
