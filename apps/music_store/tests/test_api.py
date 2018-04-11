from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from faker import Faker

from apps.users.factories import UserFactory, UserWithBalanceFactory

from ..factories import (
    AlbumFactory,
    BoughtTrackFactory,
    LikeTrackFactory,
    ListenTrackFactory,
    TrackFactoryLongFullVersion,
)
from ..models import Album, ListenTrack, Track

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
    url_liked = '/api/v1/music_store/likes/'

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
