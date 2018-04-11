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

    url = '/api/v1/music_store/tracks/'
    track = {
        'title': fake.sentence(nb_words=2),
        'price': 100500,
        'full_version': fake.sentence(nb_words=20),
    }

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    def test_forbidden_create_track_without_auth(self):
        response = self.client.post(self.url, self.track, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_track_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.track, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_free_version_of_created_track(self):
        """Test length of 'free_version' field of Track is 25"""
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.track, format='json')
        self.assertEqual(
            Track.objects.get().free_version,
            self.track['full_version'][:25]
        )

    def test_update_album_field_of_track_instance(self):
        url_albums = '/api/v1/music_store/albums/'
        album = {
            'title': fake.sentence(nb_words=2),
            'image': fake.name(),
            'price': 1005000,
            'tracks': []
        }

        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.track, format='json')
        self.client.post(url_albums, album, format='json')

        track_id = Track.objects.get().id
        album_id = Album.objects.get().id

        response = self.client.patch(
            f'{self.url}{track_id}/',
            self.track.update({'album': album_id}),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forbidden_delete_tracks_without_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.track, format='json')
        self.client.logout()

        track_to_del = Track.objects.get()
        response = self.client.delete(
            f'{self.url}{track_to_del.id}/',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tracks_with_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.track, format='json')

        track_to_del = Track.objects.get()
        response = self.client.delete(
            f'{self.url}{track_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAPIAlbum(APITestCase):
    """Test for API of 'Music Store' app.

    Tests for create and delete Albums

    """
    url = '/api/v1/music_store/albums/'
    album = {
        'title': fake.sentence(nb_words=2),
        'image': fake.name(),
        'price': 1005000,
        'tracks': []
    }

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    def test_forbidden_create_album_without_auth(self):
        response = self.client.post(self.url, self.album, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_album_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.album, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_forbidden_delete_album_without_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.album, format='json')
        self.client.logout()

        album_to_del = Album.objects.get()
        response = self.client.delete(
            f'{self.url}{album_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_album_with_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.album, format='json')

        album_to_del = Album.objects.get()
        response = self.client.delete(
            f'{self.url}{album_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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














