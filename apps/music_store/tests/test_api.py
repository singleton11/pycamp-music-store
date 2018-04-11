from rest_framework import status

from rest_framework.test import (
    APIClient,
    APITestCase,
)

from faker import Faker

from ..models import (
    Track,
    Album,
    ListenTrack,
)

from ..factories import (
    AlbumFactory,
    TrackFactory,
    LikeTrackFactory,
    ListenTrackFactory,
)

from apps.users.factories import UserFactory, UserWithBalanceFactory

fake = Faker()


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
        cls.track = TrackFactory()

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
    url = '/api/v1/music_store/likes/'

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_watch_likes_forbidden_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_likes_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_forbidden_without_auth(self):
        track_to_like = TrackFactory()
        response = self.client.post(self.url, {'track': track_to_like.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        track_to_like = TrackFactory()
        response = self.client.post(self.url, {'track': track_to_like.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_like_track_second_time(self):
        self.client.force_authenticate(user=self.user)
        track_to_like = TrackFactory()
        LikeTrackFactory(user=self.user, track=track_to_like)

        response = self.client.post(self.url, {'track': track_to_like.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_like(self):
        self.client.force_authenticate(user=self.user)
        track_to_like = TrackFactory()
        like = LikeTrackFactory(user=self.user, track=track_to_like)

        response = self.client.delete(f'{self.url}{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAPIListenTrack(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for LikeTrack

    """
    url = '/api/v1/music_store/listens/'

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_watch_listens_forbidden_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_listens_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listen_forbidden_without_auth(self):
        track_to_listen = TrackFactory()
        response = self.client.post(self.url, {'track': track_to_listen.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listen_allowed_with_auth(self):
        self.client.force_authenticate(user=self.user)
        track_to_listen = TrackFactory()
        response = self.client.post(self.url, {'track': track_to_listen.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_listen_track_second_time(self):
        self.client.force_authenticate(user=self.user)
        track_to_listen = TrackFactory()
        ListenTrackFactory(user=self.user, track=track_to_listen)

        response = self.client.post(self.url, {'track': track_to_listen.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_listen_track_multiple_times(self):
        self.client.force_authenticate(user=self.user)
        track_to_listen = TrackFactory()
        number_of_listens = 10
        for i in range(number_of_listens):
            self.client.post(self.url, {'track': track_to_listen.id})

        self.assertEqual(
            ListenTrack.objects.filter(user=self.user).count(),
            number_of_listens
        )














