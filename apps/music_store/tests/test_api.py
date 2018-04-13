from operator import methodcaller
from unittest import skip

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
    UserWithPaymentMethodFactory,
    PaymentMethodFactory,
    UserWithBalanceFactory,
    TrackFactoryLongFullVersion,
    UserWithDefaultPaymentMethodFactory)
from apps.users.factories import UserFactory

fake = Faker()


def api_url(relative_url):
    """Function to get url by relative url"""
    return '/api/v1/music_store/' + relative_url


class TestAPIMusicStorePaymentMethods(APITestCase):
    """Test for payments API of ``music_store`` app. """

    def test_payment_methods_empty_list(self):
        """ Checking the display of an empty payment methods list """
        user = UserFactory()
        response = self._api_payment_method(None, user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_payment_methods_list(self):
        """ Checking that the user sees only their purchased tracks """
        user = UserWithPaymentMethodFactory()
        PaymentMethodFactory(owner=user)
        PaymentMethodFactory()

        response = self._api_payment_method(None, user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_payment_methods_not_auth_get(self):
        """ Unauthorized user verification """
        response = self._api_payment_method(data=None, user=None, method='get')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_payment_methods_add_new(self):
        """ Checking the purchase result code """
        user = UserFactory()
        data = {
            'title': "New method",
            'is_default': True,
        }
        response = self._api_payment_method(data, user)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_payment_methods_patch_edit(self):
        """ Edit a part of payment method with patch request """
        payment_method = PaymentMethodFactory()
        data = {'is_default': True}

        self.client.force_authenticate(user=payment_method.owner)
        url = api_url(f'payment_methods/{payment_method.pk}/')
        response = self.client.patch(url, data)
        self.assertTrue(response.data['is_default'])

    def test_payment_methods_put_edit(self):
        """ Edit a part of payment method with put request """
        payment_method = PaymentMethodFactory()
        data = {'is_default': True, 'title': 'test'}

        self.client.force_authenticate(user=payment_method.owner)
        url = api_url(f'payment_methods/{payment_method.pk}/')
        response = self.client.put(url, data)
        self.assertEqual(response.data, data)

    def test_payment_methods_delete(self):
        """ Delete payment method """
        payment_method = PaymentMethodFactory()
        self.client.force_authenticate(user=payment_method.owner)
        url = api_url(f'payment_methods/{payment_method.pk}/')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_payment_methods_delete_not_own_method(self):
        """ Trying to delete not your own payment method """
        user = UserFactory()
        payment_method = PaymentMethodFactory()
        self.client.force_authenticate(user=user)
        url = api_url(f'payment_methods/{payment_method.pk}/')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def _api_payment_method(self, data, user=None, method="post"):
        """ Method for send request to PaymentMethod Api """
        if user:
            self.client.force_authenticate(user=user)

        url = api_url('payment_methods/')
        caller = methodcaller(method, url, data)
        return caller(self.client)


class TestAPITrack(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for create, update and delete Tracks

    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    @classmethod
    def setUpTestData(cls):
        cls.url = api_url('tracks/')
        cls.track = TrackFactoryLongFullVersion()

    def test_get_list_of_tracks_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_tracks_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_track_without_auth(self):
        response = self.client.get(f'{self.url}{self.track.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_track_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.track.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_of_track_no_login(self):
        """If not logged in, content is free version"""
        response = self.client.get(f'{self.url}{self.track.id}/')
        content = response.data['content']
        self.assertEqual(
            content,
            self.track.free_version
        )

    def test_content_of_track_login_not_bought(self):
        """If logged in and track not bought, content is free version"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.track.id}/')
        content = response.data['content']
        self.assertEqual(
            content,
            self.track.free_version
        )

    def test_content_of_track_login_bought(self):
        """If logged in and track bought, content is full version"""
        self.client.force_authenticate(user=self.user)
        BoughtTrackFactory(user=self.user, item=self.track)

        response = self.client.get(f'{self.url}{self.track.id}/')
        content = response.data['content']
        self.assertEqual(
            content,
            self.track.full_version
        )


class TestAPIAlbum(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for create and delete Albums

    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    @classmethod
    def setUpTestData(cls):
        cls.url = api_url('albums/')
        cls.album = AlbumFactory()

    def test_get_list_of_albums_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_albums_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_album_without_auth(self):
        response = self.client.get(f'{self.url}{self.album.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_album_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.album.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAPILikeTrack(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for LikeTrack

    """
    url_liked = api_url('liked/')

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_watch_likes_forbidden_without_auth(self):
        response = self.client.get(self.url_liked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_likes_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_liked)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_forbidden_without_auth(self):
        pass

    def test_like_allowed_with_auth(self):
        pass

    def test_cannot_like_track_second_time(self):
        pass

    def test_dislike(self):
        pass


class TestAPIListenTrack(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for LikeTrack

    """
    url_listened = api_url('listened/')

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_watch_listens_forbidden_without_auth(self):
        response = self.client.get(self.url_listened)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_listens_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_listened)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listen_forbidden_without_auth(self):
        pass

    def test_listen_allowed_with_auth(self):
        pass

    def test_can_listen_track_second_time(self):
        pass

    def test_can_listen_track_multiple_times(self):
        pass


class TestAPIMusicStoreBoughtTrack(APITestCase):
    """Test for API of ``music_store`` app for bought track. """

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithDefaultPaymentMethodFactory(balance=100)

        self.track = TrackFactory(price=10)
        self.track_high_price = TrackFactory(price=1000)

    def test_bought_track_empty_list(self):
        """ Checking the display of an empty track list"""
        response = self._api_bougth_track(None, self.user, method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @skip("need fix")
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

    @skip("need fix")
    def test_bought_track_buy_result_code(self):
        """ Checking the purchase result code"""
        data = {'item': self.track.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @skip("need fix")
    def test_bought_track_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance

        data = {'item': self.track.pk}
        self._api_bougth_track(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.track.price)

    @skip("need fix")
    def test_bought_track_buy_not_enough_money(self):
        """ Trying to buy a track for which there is not enough money"""
        data = {'item': self.track_high_price.pk}
        response = self._api_bougth_track(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    @skip("need fix")
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

    @skip("need fix")
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

    @skip("need fix")
    def test_bought_album_buy_result_code(self):
        """ Checking the purchase result code"""
        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @skip("need fix")
    def test_bought_album_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance

        data = {'item': self.album.pk}
        self._api_bougth_album(data, self.user)

        self.assertEqual(self.user.balance, balance_before - self.album.price)

    @skip("need fix")
    def test_bought_album_buy_not_enough_money(self):
        """ Trying to buy a album for which there is not enough money"""
        data = {'item': self.album_high_price.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    @skip("need fix")
    def test_bought_already_exists_album(self):
        """ Trying to buy an already purchased album"""
        BoughtAlbumFactory(user=self.user, item=self.album)

        data = {'item': self.album.pk}
        response = self._api_bougth_album(data, self.user)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _api_bougth_album(self, data, user=None, method="post"):
        """ Method for send request to BoughtAlbum Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url('bought_albums/')
        caller = methodcaller(method, url, data)
        return caller(self.client)
