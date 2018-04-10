import tempfile
import unittest
from operator import methodcaller

from django.test import override_settings

from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from faker import Faker

from apps.music_store.factories import TrackFactory
from ..api.views import (
    BoughtTrackViewSet
)
from apps.users.factories import UserWithBalanceFactory

fake = Faker()


@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class TestAPIMusicStoreBoughtItems(APITestCase):
    """Test for API of ``music_store`` app. """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.track = TrackFactory(price=10)
        self.track_high_price = TrackFactory(price=1000)
        self.user = UserWithBalanceFactory(balance=100)

    def test_bought_track_empty_list(self):
        url = '/api/v1/music_store/bought_tracks/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = BoughtTrackViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bought_track_buy_result_code(self):
        data = {'item': self.track.pk}

        url = '/api/v1/music_store/bought_tracks/'
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)

        response = BoughtTrackViewSet.as_view({'post': 'create'})(request)
        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_bought_track_buy_sub_balance(self):
        balance_before = self.user.balance

        data = {'item': self.track.pk}

        url = '/api/v1/music_store/bought_tracks/'
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)

        BoughtTrackViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(self.user.balance, balance_before - self.track.price)

    def test_bought_track_buy_not_enough_money(self):
        data = {'item': self.track_high_price.pk}

        url = '/api/v1/music_store/bought_tracks/'
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)

        response = BoughtTrackViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_cod, status.HTTP_400_BAD_REQUEST)
