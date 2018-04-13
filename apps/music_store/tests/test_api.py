from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from faker import Faker

from apps.users.factories import UserFactory, UserWithBalanceFactory

from ..factories import (
    AlbumFactory,
    BoughtTrackFactory,
    LikeTrackFactory,
    TrackFactoryLongFullVersion,
)

fake = Faker()


class TestAPITrack(APITestCase):
    """Tests for Tracks API."""
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.user_with_balance = UserWithBalanceFactory()
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
    """Tests for Albums API."""
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


class TestAPILikeTrackListView(APITestCase):
    """Tests for API list of liked tracks."""

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/music_store/liked/'
        cls.count = 2
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.likes = [LikeTrackFactory(user=cls.user) for i in range(cls.count)]
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
        cls.url = '/api/v1/music_store/tracks/'
        cls.count = 2
        cls.client = APIClient()
        cls.user = UserFactory()
        cls.likes = [LikeTrackFactory(user=cls.user) for i in range(cls.count)]
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
        cls.url = '/api/v1/music_store/listened/'
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
