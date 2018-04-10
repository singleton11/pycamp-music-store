from rest_framework import status

from rest_framework.test import (
    APIClient,
    APITestCase,
)

from faker import Faker

from ..api.views import (
    LikeTrackViewSet,
    ListenTrackViewSet,
    AlbumViewSet,
    TrackViewSet,
)

from ..models import (
    Track,
    Album,
)

from apps.users.factories import UserFactory, UserWithBalanceFactory

fake = Faker()

url_tracks = '/api/v1/music_store/tracks/'
track = {
    'title': fake.sentence(nb_words=2),
    'price': 100500,
    'full_version': fake.sentence(nb_words=20),
}

url_albums = '/api/v1/music_store/albums/'
album = {
    'title': fake.sentence(nb_words=2),
    'image': fake.name(),
    'price': 1005000,
    'tracks': []
}


class TestAPITrack(APITestCase):
    """Test for API of 'Music Store' app.



    """
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    def test_forbidden_create_track_without_auth(self):
        response = self.client.post(url_tracks, track, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_track_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url_tracks, track, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_free_version_of_created_track(self):
        """Test length of 'free_version' field of Track is 25"""
        self.client.force_authenticate(user=self.user)
        self.client.post(url_tracks, track, format='json')
        self.assertEqual(
            Track.objects.get().free_version,
            track['full_version'][:25]
        )

    def test_update_album_field_of_track_instance(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(url_tracks, track, format='json')
        self.client.post(url_albums, album, format='json')

        track_id = Track.objects.get().id
        album_id = Album.objects.get().id

        response = self.client.patch(
            f'{url_tracks}{track_id}/',
            track.update({'album': album_id}),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forbidden_delete_tracks_without_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(url_tracks, track, format='json')
        self.client.logout()

        track_to_del = Track.objects.get()
        response = self.client.delete(
            f'{url_tracks}{track_to_del.id}/',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tracks_with_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(url_tracks, track, format='json')

        track_to_del = Track.objects.get()
        response = self.client.delete(
            f'{url_tracks}{track_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAPIAlbum(APITestCase):
    """Test for API of 'Music Store' app.



    """
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_with_balance = UserWithBalanceFactory()

    def test_forbidden_create_album_without_auth(self):
        response = self.client.post(url_albums, album, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_album_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url_albums, album, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_forbidden_delete_album_without_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(url_albums, album, format='json')
        self.client.logout()

        album_to_del = Album.objects.get()
        response = self.client.delete(
            f'{url_albums}{album_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_album_with_login(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(url_albums, album, format='json')

        album_to_del = Album.objects.get()
        response = self.client.delete(
            f'{url_albums}{album_to_del.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



