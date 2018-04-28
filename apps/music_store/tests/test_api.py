from operator import methodcaller

from faker import Faker
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from apps.users.factories import UserFactory
from ..factories import (
    AlbumFactory,
    BoughtTrackFactory,
    LikeTrackFactory,
    TrackFactoryLongFullVersion,
    TrackFactory,
    BoughtAlbumFactory,
    UserWithPaymentMethodFactory,
    PaymentMethodFactory,
    UserWithBalanceFactory,
    TrackWithoutAlbumFactory
)
from apps.music_store.api.serializers import TrackSerializer

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
    """Tests for Tracks API."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.user_with_balance = UserWithBalanceFactory()
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
    """Tests for Albums API."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.user_with_balance = UserWithBalanceFactory()
        cls.url = api_url('albums/')
        cls.album = AlbumFactory()
        cls.tracks = TrackFactory.create_batch(3, album=cls.album)

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

    def test_get_track_list_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.album.id}/track_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            TrackSerializer(self.tracks, many=True).data
        )


class TestAPILikeTrackListView(APITestCase):
    """Tests for API list of liked tracks."""

    @classmethod
    def setUpTestData(cls):
        cls.url = api_url('liked/')
        cls.count = 2
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.likes = LikeTrackFactory.create_batch(cls.count, user=cls.user)
        cls.track_to_like = TrackFactoryLongFullVersion()

    def test_watch_likes_forbidden_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_likes_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAPILikeUnlikeTrack(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = api_url('tracks/')
        cls.count = 2
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.likes = LikeTrackFactory.create_batch(cls.count, user=cls.user)
        cls.track_to_like = TrackFactoryLongFullVersion()

    def test_like_forbidden_without_auth(self):
        response = self.client.post(
            f'{self.url}{self.track_to_like.id}/like/'
        )
        self.assertTrue(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_like_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'{self.url}{self.track_to_like.id}/like/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(self.track_to_like.is_liked(self.user))

    def test_unlike_forbidden_without_auth(self):
        LikeTrackFactory(user=self.user, track=self.track_to_like)
        response = self.client.delete(
            f'{self.url}{self.track_to_like.id}/like/'
        )
        self.assertTrue(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_unlike_allowed_with_auth(self):
        LikeTrackFactory(user=self.user, track=self.track_to_like)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f'{self.url}{self.track_to_like.id}/like/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertFalse(self.track_to_like.is_liked(self.user))

    def test_cannot_unlike_not_liked_track(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f'{self.url}{self.track_to_like.id}/like/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class TestAPIListenTrackListView(APITestCase):
    """Tests for API list of listened tracks."""

    @classmethod
    def setUpTestData(cls):
        cls.url = api_url('listened/')
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.track_to_listen = TrackFactoryLongFullVersion()

    def test_watch_listens_forbidden_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_listens_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAPIListenTrack(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/music_store/tracks/'
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.track_to_listen = TrackFactoryLongFullVersion()

    def test_listen_forbidden_without_auth(self):
        response = self.client.post(
            f'{self.url}{self.track_to_listen.id}/listen/'
        )
        self.assertTrue(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_listen_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'{self.url}{self.track_to_listen.id}/listen/'
        )
        self.assertTrue(
            response.status_code,
            status.HTTP_200_OK
        )


class TestAPIMusicStoreBoughtTrack(APITestCase):
    """Test for API of ``music_store`` app for bought track. """

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithBalanceFactory(balance=100)

        self.track = TrackFactory(price=10)
        self.track_high_price = TrackFactory(price=1000)

    def test_bought_track_empty_list(self):
        """ Checking the display of an empty track list"""
        response = self._api_list_bought_track(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_bought_track_list(self):
        """ Checking that the user sees only their purchased tracks"""
        BoughtTrackFactory()
        BoughtTrackFactory(user=self.user, item=self.track)
        BoughtTrackFactory(user=self.user, item=self.track_high_price)

        response = self._api_list_bought_track(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_track_buy_not_auth_get(self):
        """ Unauthorized user verification"""
        response = self._api_buy_track(self.track.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_track_buy_result_code(self):
        """ Checking the purchase result code"""
        response = self._api_buy_track(self.track.pk, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_track_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance
        self._api_buy_track(self.track.pk, self.user)
        self.assertEqual(self.user.balance, balance_before - self.track.price)

    def test_track_buy_not_enough_money(self):
        """ Trying to buy a track for which there is not enough money"""
        response = self._api_buy_track(self.track_high_price.pk, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_already_exists_track(self):
        """ Trying to buy an already purchased track"""
        BoughtTrackFactory(user=self.user, item=self.track)

        balance_before = self.user.balance
        response = self._api_buy_track(self.track.pk, self.user)
        balance_after = self.user.balance

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(balance_before, balance_after)

    def test_track_buy_not_default_method(self):
        """ Checking the purchase result code"""
        method = PaymentMethodFactory(owner=self.user)

        response = self._api_buy_track(self.track.pk, self.user, method.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _api_buy_track(self, item_id, user=None, payment_id=None):
        """ Method for send request to bought Track Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url(f'tracks/{item_id}/buy/')
        if payment_id:
            url = url + "?payment_id=" + str(payment_id)
        return self.client.post(url)

    def _api_list_bought_track(self, user=None):
        """ Method for send request to bought Track Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url(f'bought_tracks/')
        return self.client.get(url)


class TestAPIMusicStoreBoughtAlbum(APITestCase):
    """Test for API of ``music_store`` app for bought album."""

    def setUp(self):
        self.client = APIClient()
        self.user = UserWithBalanceFactory(balance=100)

        self.album = AlbumFactory(price=10)
        self.album_high_price = AlbumFactory(price=1000)

    def test_bought_album_empty_list(self):
        """ Checking the display of an empty album list"""
        response = self._api_list_bought_album(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_bought_album_list(self):
        """ Checking that the user sees only their purchased albums"""
        BoughtAlbumFactory()
        BoughtAlbumFactory(user=self.user, item=self.album)
        BoughtAlbumFactory(user=self.user, item=self.album_high_price)

        response = self._api_list_bought_album(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_album_buy_not_auth_get(self):
        """ Unauthorized user verification"""
        response = self._api_buy_album(self.album.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_album_buy_result_code(self):
        """ Checking the purchase result code"""
        response = self._api_buy_album(self.album.pk, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_album_buy_sub_balance(self):
        """ Checking the reduction of balance after purchase"""
        balance_before = self.user.balance

        self._api_buy_album(self.album.pk, self.user)
        self.assertEqual(self.user.balance, balance_before - self.album.price)

    def test_album_buy_not_enough_money(self):
        """ Trying to buy a album for which there is not enough money"""
        response = self._api_buy_album(self.album_high_price.pk, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_already_exists_album(self):
        """ Trying to buy an already purchased album"""
        BoughtAlbumFactory(user=self.user, item=self.album)

        balance_before = self.user.balance
        response = self._api_buy_album(self.album.pk, self.user)
        balance_after = self.user.balance

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(balance_before, balance_after)

    def _api_buy_album(self, item_id, user=None):
        """ Method for send request to buy Album Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url(f'albums/{item_id}/buy/')
        return self.client.post(url)

    def _api_list_bought_album(self, user=None):
        """ Method for send request to buy Album Api"""
        if user:
            self.client.force_authenticate(user=self.user)

        url = api_url(f'bought_albums/')
        return self.client.get(url)


class TestAPISearch(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for search tracks and albums

    """

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.track_1 = TrackWithoutAlbumFactory(
            title="one two",
            author="three four",
        )
        cls.track_2 = TrackWithoutAlbumFactory(
            title="one",
            author="five",
        )
        cls.track_3 = TrackWithoutAlbumFactory(
            title="six",
            author="two",
        )
        cls.track_4 = TrackWithoutAlbumFactory(
            title="unique1",
            author="unique2",
        )

        cls.album_1 = AlbumFactory(
            title="one two",
            author="three four",
        )
        cls.album_2 = AlbumFactory(
            title="one",
            author="five",
        )
        cls.album_3 = AlbumFactory(
            title="six",
            author="two",
        )
        cls.album_4 = AlbumFactory(
            title="unique3",
            author="unique4",
        )

        cls.url = '/api/v1/music_store/'

    def test_search_tracks_many_1(self):
        response = self.client.get(self.url + 'tracks/?search=one')
        self.assertEqual(len(response.data), 2)

    def test_search_tracks_many_2(self):
        response = self.client.get(self.url + 'tracks/?search=two')
        self.assertEqual(len(response.data), 2)

    def test_search_tracks_one_1(self):
        response = self.client.get(self.url + 'tracks/?search=ix')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.track_3.id)

    def test_search_tracks_one_2(self):
        response = self.client.get(self.url + 'tracks/?search=ive')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.track_2.id)

    def test_search_albums_many_1(self):
        response = self.client.get(self.url + 'albums/?search=one')
        self.assertEqual(len(response.data), 2)

    def test_search_albums_many_2(self):
        response = self.client.get(self.url + 'albums/?search=two')
        self.assertEqual(len(response.data), 2)

    def test_search_albums_one_1(self):
        response = self.client.get(self.url + 'albums/?search=ix')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.album_3.id)

    def test_search_albums_one_2(self):
        response = self.client.get(self.url + 'albums/?search=ive')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.album_2.id)

    def test_global_search_unique_track(self):
        response = self.client.get(self.url + 'search/?query=unique1')
        tracks = response.data['tracks']
        albums = response.data['albums']
        self.assertEqual(len(tracks), 1)
        self.assertEqual(len(albums), 0)
        self.assertEqual(tracks[0].get('id'), self.track_4.id)

    def test_global_search_unique_album(self):
        response = self.client.get(self.url + 'search/?query=unique3')
        tracks = response.data['tracks']
        albums = response.data['albums']
        self.assertEqual(len(tracks), 0)
        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0].get('id'), self.album_4.id)

    def test_global_search_many(self):
        response = self.client.get(self.url + 'search/?query=one')
        tracks = response.data['tracks']
        albums = response.data['albums']
        self.assertEqual(len(tracks), 2)
        self.assertEqual(len(albums), 2)
