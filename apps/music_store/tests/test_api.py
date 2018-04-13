from operator import methodcaller

from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.music_store.factories import (
    UserWithPaymentMethodFactory,
    PaymentMethodFactory,
    UserWithBalanceFactory,
    TrackWithoutAlbumFactory)
from apps.users.factories import UserFactory
from ..factories import (
    AlbumFactory,
    BoughtTrackFactory,
    TrackFactoryLongFullVersion,
)

fake = Faker()


class TestAPIMusicStorePaymentMethods(APITestCase):
    """Test for payments API of ``music_store`` app. """

    def _url(self, sub_url):
        return '/api/v1/music_store/' + sub_url

    def _api_payment_method(self, data, user=None, method="post"):
        """ Method for send request to PaymentMethod Api """
        if user:
            self.client.force_authenticate(user=user)

        url = self._url('payment_methods/')
        caller = methodcaller(method, url, data)
        return caller(self.client)

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
        url = self._url(f'payment_methods/{payment_method.pk}/')
        response = self.client.patch(url, data)
        self.assertTrue(response.data['is_default'])

    def test_payment_methods_put_edit(self):
        """ Edit a part of payment method with put request """
        payment_method = PaymentMethodFactory()
        data = {'is_default': True, 'title': 'test'}

        self.client.force_authenticate(user=payment_method.owner)
        url = self._url(f'payment_methods/{payment_method.pk}/')
        response = self.client.put(url, data)
        self.assertEqual(response.data, data)

    def test_payment_methods_delete(self):
        """ Delete payment method """
        payment_method = PaymentMethodFactory()
        self.client.force_authenticate(user=payment_method.owner)
        url = self._url(f'payment_methods/{payment_method.pk}/')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_payment_methods_delete_not_own_method(self):
        """ Trying to delete not your own payment method """
        user = UserFactory()
        payment_method = PaymentMethodFactory()
        self.client.force_authenticate(user=user)
        url = self._url(f'payment_methods/{payment_method.pk}/')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        cls.url = '/api/v1/music_store/tracks/'
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
        cls.url = '/api/v1/music_store/albums/'
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
    url_liked = '/api/v1/music_store/liked/'

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

    Tests for ListenTrack

    """
    url_listened = '/api/v1/music_store/listened/'

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
