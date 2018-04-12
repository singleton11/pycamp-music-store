from operator import methodcaller
from rest_framework import status
from rest_framework.test import APITestCase

from apps.music_store.factories import (
    UserWithPaymentMethodFactory, PaymentMethodFactory)
from apps.users.factories import UserFactory


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
