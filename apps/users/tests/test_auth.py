import faker
import unittest
from django.test import override_settings
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site

from allauth.account.tests import TestCase
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.helpers import complete_social_login
from unittest.mock import patch, Mock

from ..adapter import SocialAccountAdapter
from ..factories import UserFactory

fake = faker.Faker()


class SocialAccountAdapterTests(TestCase):

    def setUp(self):
        super(SocialAccountAdapterTests, self).setUp()

        site = Site.objects.get_current()
        self.factory = RequestFactory()
        self.user = UserFactory()

    def _get_request(self, user=None):
        user = user or self.user
        request = self.factory.get('/')
        request.user = user

        SessionMiddleware().process_request(request)

        return request

    def _make_email(self, email, user, primary=True, verified=True):
        return EmailAddress.objects.create(email=email, verified=verified,
                                           primary=primary, user=user)

    def _make_social_login(self, user, emails, uid, provider='openid'):
        account = SocialAccount(provider=provider, uid=uid)
        return SocialLogin(user=user, account=account, email_addresses=emails)

    def assertConnectNotCalled(self, request, sociallogin):
        """Shortcut for cheking ``connect`` method of ``sociallogin`` not
        called
        """
        with patch.object(sociallogin, 'connect') as connect_method:
            adapter = SocialAccountAdapter()
            adapter.pre_social_login(request, sociallogin)
            connect_method.assert_not_called()

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory')
    def test_social_auth_verified_email(self):
        request = self._get_request()
        user = request.user
        uid = '999'

        email = self._make_email(user.email, user)
        sociallogin = self._make_social_login(user, (email,), uid=uid)
        complete_social_login(request, sociallogin)

        self.assertTrue(
            SocialAccount.objects.filter(user=user, uid=uid).exists()
        )

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory')
    def test_social_auth_without_emails(self):
        request = self._get_request()
        uid = '999'

        sociallogin = self._make_social_login(request.user, (), uid=uid)
        self.assertConnectNotCalled(request, sociallogin)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory')
    def test_social_auth_with_not_verified_email(self):
        request = self._get_request()
        user = request.user
        uid = '999'

        email = self._make_email(user.email, user, verified=False)
        sociallogin = self._make_social_login(request.user, (email,), uid=uid)
        self.assertConnectNotCalled(request, sociallogin)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory')
    def test_social_auth_with_not_verified_email(self):
        request = self._get_request()
        user = request.user
        uid = '999'

        email = self._make_email('bad-email@email.em', user, verified=False)
        sociallogin = self._make_social_login(request.user, (email,), uid=uid)

        self.assertConnectNotCalled(request, sociallogin)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory')
    @unittest.skip("FIX")
    def test_social_auth_with_several_emails(self):
        request = self._get_request()
        user = request.user
        uid = '999'

        email1 = self._make_email('old-email@em.em', user, verified=False)
        email2 = self._make_email(user.email, user, verified=True)
        sociallogin = self._make_social_login(request.user, (email1, email2),
                                              uid=uid)

        with patch.object(sociallogin, 'connect') as connect_method:
            adapter = SocialAccountAdapter()
            adapter.pre_social_login(request, sociallogin)
            connect_method.assert_called_once_with(request, user)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=None)
    def test_social_auth_with_not_existed_emails(self):
        request = self._get_request()
        user = request.user
        uid = '999'

        email = Mock()
        email.email = 'not-existed@ema.il'
        email.user = user
        email.verified = False
        sociallogin = self._make_social_login(user, (email, ), uid=uid)

        self.assertConnectNotCalled(request, sociallogin)
