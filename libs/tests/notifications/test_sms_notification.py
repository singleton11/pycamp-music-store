from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

from ...notifications import SMSNotification


class MockTwilioMessages(object):
    def create(self, to, from_, body):
        pass


class MockTwilio(object):
    messages = MockTwilioMessages()


class SMSNotificationTestCase(TestCase):
    """Test case for ``SMSNotification``"""

    def setUp(self):
        self.sms_notification = SMSNotification()

    def test_init(self):
        """Test ``__init__`` called without args should set
        ``context_variables`` to ``{}``"""
        self.assertEqual(self.sms_notification.context_variables, {})

    def test_get_from(self):
        """Test ``get_from_`` method"""
        self.sms_notification.from_ = 'test'
        self.assertEqual(
            self.sms_notification.get_from_(),
            self.sms_notification.from_
        )

    @override_settings(TWILIO_FROM_NUMBER=1)
    def test_get_from_is_not_set(self):
        """Test ``get_from_`` when from is not set, should use settings
        value"""
        self.assertEqual(
            self.sms_notification.get_from_(),
            settings.TWILIO_FROM_NUMBER
        )

    def test_get_to(self):
        """Test ``get_to`` method"""
        self.sms_notification.to = 'test'
        self.assertEqual(
            self.sms_notification.get_to(),
            self.sms_notification.to
        )

    def test_get_context_variables(self):
        """Test ``get_context_variables``"""
        context_variables = {}
        sms_notification = SMSNotification(context_variables=context_variables)
        self.assertEqual(
            sms_notification.get_context_variables(),
            context_variables
        )

    @patch('django.template.loader.get_template')
    def test_get_body(self, get_template):
        """Test ``get_body`` when ``body`` attribute is not set"""
        self.sms_notification.get_body()
        get_template.assert_called_once_with(
            '{}.txt'.format(self.sms_notification.get_template_name()),
            using=None
        )

    def test_get_body_set(self):
        """Test ``get_body`` when ``body`` attribute is set"""
        self.sms_notification.body = 'test'
        self.assertEqual(
            self.sms_notification.get_body(),
            self.sms_notification.body
        )

    @override_settings(TWILIO_FROM_NUMBER=1)
    @override_settings(TWILIO=MockTwilio())
    @patch('libs.tests.notifications.test_sms_notification.MockTwilioMessages.create')
    @patch('django.template.loader.get_template')
    def test_send(self, get_template, create):
        """Test ``send`` should call ``create`` from
        ``settings.TWILIO.messages``"""
        self.sms_notification.to = 'test'
        self.sms_notification.send()
        self.assertEqual(
            create.call_args_list[0][1]['from_'],
            self.sms_notification.get_from_()
        )
        self.assertEqual(
            create.call_args_list[0][1]['to'],
            self.sms_notification.to
        )

    @override_settings(TWILIO_FROM_NUMBER=1)
    @override_settings(TWILIO=MockTwilio())
    @patch(
        'libs.tests.notifications.test_sms_notification.MockTwilioMessages.create')
    @patch('django.template.loader.get_template')
    def test_send_through_args(self, get_template, create):
        """Test arguments transfer: data should be obtained from arguments"""
        to = 1
        from_ = 'test'
        body = 'test'
        self.sms_notification.send(to=to, from_=from_, body=body)
        create.assert_called_with(body=body, from_=from_, to=to)

    @override_settings(TWILIO_FROM_NUMBER=1)
    @override_settings(TWILIO=MockTwilio())
    @patch(
        'libs.tests.notifications.test_sms_notification.MockTwilioMessages.create')
    @patch('libs.notifications.SMSNotification.get_body', return_value=None)
    def test_send_no_body(self, get_body, create):
        """Test ``send`` with no ``body``, should raises ``ValueError``"""
        with self.assertRaises(ValueError):
            self.sms_notification.send()

    @override_settings(TWILIO_FROM_NUMBER=1)
    @override_settings(TWILIO=MockTwilio())
    @patch(
        'libs.tests.notifications.test_sms_notification.MockTwilioMessages.create')
    @patch('libs.notifications.SMSNotification.get_from_', return_value=None)
    @patch('django.template.loader.get_template')
    def test_send_no_from(self, get_template, get_from, create):
        """Test ``send`` with no ``from_``, should raises ``ValueError``"""
        with self.assertRaises(ValueError):
            self.sms_notification.send()

    @override_settings(TWILIO_FROM_NUMBER=1)
    @override_settings(TWILIO=MockTwilio())
    @patch(
        'libs.tests.notifications.test_sms_notification.MockTwilioMessages.create')
    @patch('libs.notifications.SMSNotification.get_to', return_value=None)
    @patch('django.template.loader.get_template')
    def test_send_no_to(self, get_template, get_to, create):
        """Test ``send`` with no ``to``, should raises ``ValueError``"""
        with self.assertRaises(ValueError):
            self.sms_notification.send()
