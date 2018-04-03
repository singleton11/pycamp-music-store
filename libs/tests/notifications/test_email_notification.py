from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

from libs.notifications import EmailNotification


class NotificationsTestCase(TestCase):
    """Tests for notification classes from ``libs``"""

    def setUp(self):
        self.email_notification = EmailNotification()
        self.email_notification.body_text = 'test'
        self.email_notification.body_html = 'test'
        self.email_notification.subject = 'test'
        self.email_notification.to_emails = 'test'
        self.email_notification.bcc = ('test',)
        self.email_notification.reply_to = 'test'
        self.email_notification.extra_headers = {}

    def test_context_variables_is_not_set(self):
        """Test ``__init__`` arg ``context_variables`` is not transferred,
        should return ``{}``"""
        self.assertEqual(self.email_notification.context_variables, {})

    def test_get_subject(self):
        """Test ``get_subject`` method"""
        self.assertEqual(self.email_notification.get_subject(), 'test')

    def test_get_from_email(self):
        """Test ``get_from_email`` when ``EmailNotification.from_email`` is
        not set"""
        self.assertEqual(
            self.email_notification.get_from_email(),
            settings.DEFAULT_FROM_EMAIL
        )

    def test_get_from_email_set(self):
        """Test ``get_from_email`` when ``EmailNotification.from_email`` is
        set"""
        self.email_notification.from_email = 'test@test.test'
        self.assertEqual(
            self.email_notification.get_from_email(),
            self.email_notification.from_email
        )

    def test_get_to_emails(self):
        """Test ``get_to_emails`` should return ``to_emails`` attribute"""
        self.assertEqual(self.email_notification.get_to_emails(), 'test')

    def test_get_context_variables(self):
        """Test ``get_context_variables`` should return context_variables,
        which set from ``__init__`` method"""
        context_variables = {'test': 'test'}
        email_notifications = EmailNotification(
            context_variables=context_variables
        )
        self.assertEqual(
            email_notifications.get_context_variables(),
            context_variables
        )

    def test_get_template_name(self):
        """Test ``get_template_name`` regular expression ``sub``"""
        self.assertEqual(
            self.email_notification.get_template_name(),
            'email_notification'
        )

    def test_get_template_name_attribute_is_set(self):
        """Test ``get_template_name`` if ``template_name`` was set"""
        self.email_notification.template_name = 'test'
        self.assertEqual(
            self.email_notification.get_template_name(),
            self.email_notification.template_name
        )

    def test_get_body_set(self):
        """Test body getting from ``body_text/html`` attribute"""
        self.assertEqual(
            self.email_notification.get_body_text(),
            self.email_notification.body_text
        )
        self.assertEqual(
            self.email_notification.get_body_html(),
            self.email_notification.body_text
        )

    @patch('django.template.loader.get_template')
    def test_get_body_text(self, get_template):
        """Test body getting when ``body_text/html`` attribute is not set"""
        self.email_notification.body_text = None
        self.email_notification.body_html = None
        self.email_notification.get_body_text()
        get_template.assert_called_with(
            '{}.txt'.format(self.email_notification.get_template_name()),
            using=None
        )

        self.email_notification.get_body_html()
        get_template.assert_called_with(
            '{}.html'.format(self.email_notification.get_template_name()),
            using=None
        )

    def test_get_bcc(self):
        """Test get bcc from attribute"""
        self.assertEqual(
            self.email_notification.get_bcc(),
            self.email_notification.bcc
        )

    def test_get_reply_to(self):
        """Test ``get_reply_to`` returns ``reply_to`` attribute value"""
        self.assertEqual(
            self.email_notification.get_reply_to(),
            self.email_notification.reply_to
        )

    def test_get_extra_headers(self):
        """Test ``get_extra_headers`` returns ``extra_headers`` attribute
        value"""
        self.assertEqual(
            self.email_notification.get_extra_headers(),
            self.email_notification.extra_headers
        )

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    def test_send_email_to_one_recepient(self, get_template, attach, send,
                                         backend):
        """Test that ``send`` calls ``EmailMultiAlternatives.__init__``"""
        with patch('django.core.mail.EmailMultiAlternatives.__init__',
                   return_value=None) as init:
            self.email_notification.send()
            init.assert_called_once_with(
                bcc=self.email_notification.bcc,
                body=self.email_notification.body_text,
                connection=None,
                from_email=settings.DEFAULT_FROM_EMAIL,
                headers={'Reply-To': self.email_notification.reply_to},
                subject=self.email_notification.subject,
                to=[self.email_notification.to_emails]
            )

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    def test_send_email_to_many_recepients(self, get_template, attach, send,
                                           backend):
        """Test ``send`` with few recipients"""
        self.email_notification.reply_to = 'test'
        self.email_notification.to_emails = ['test', 'test']
        with patch('django.core.mail.EmailMultiAlternatives.__init__',
                   return_value=None) as init:
            self.email_notification.send()
            init.assert_called_once_with(
                bcc=self.email_notification.bcc,
                body=self.email_notification.body_text,
                connection=None,
                from_email=settings.DEFAULT_FROM_EMAIL,
                headers={'Reply-To': self.email_notification.reply_to},
                subject=self.email_notification.subject,
                to=self.email_notification.to_emails
            )

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    def test_send_email_with_no_subject(self, get_template, attach, send,
                                        backend):
        """Test ``send`` with no subject, should raises ``ValueError``"""
        self.email_notification.subject = None
        with self.assertRaises(ValueError):
            self.email_notification.send()

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    @patch('libs.notifications.EmailNotification.get_body_text',
           return_value=None)
    def test_send_email_with_no_body_text(self, get_template, attach, send,
                                          backend, get_body_text):
        """Test ``send`` with no ``body_text``, should raises
        ``ValueError``"""
        self.email_notification.body_text = None
        with self.assertRaises(ValueError):
            self.email_notification.send()

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    def test_send_email_with_no_subject(self, get_template, attach, send,
                                        backend):
        """Test ``send`` with no subject, should raises ``ValueError``"""
        self.email_notification.subject = None
        with self.assertRaises(ValueError):
            self.email_notification.send()

    @patch('django.template.loader.get_template')
    @patch('django.core.mail.EmailMultiAlternatives.attach_alternative')
    @patch('django.core.mail.EmailMultiAlternatives.send')
    @patch('django.core.mail.backends.locmem.EmailBackend', return_value=None)
    @override_settings(DEFAULT_FROM_EMAIL=None)
    def test_send_email_with_no_from(self, get_template, attach, send,
                                     backend):
        """Test ``send`` with no ``from_email``, should raises
        ``ValueError``"""
        self.email_notification.from_email = None
        with self.assertRaises(ValueError):
            self.email_notification.send()
