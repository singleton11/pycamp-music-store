from django.test import TestCase

from ...notifications import SendgridTemplateEmailNotification


class SendGridTemplateEmailNotificationTestCase(TestCase):
    """Test case for ``SendgridTemplateEmailNotification``"""

    def setUp(self):
        self.email_notification = SendgridTemplateEmailNotification()
        self.email_notification.template_id = 1
        self.email_notification._to_emails = None
        self.email_notification._bcc = None

    def test_get_template_id(self):
        """Test ``get_template_id`` method, should return ``template_id``
        attribute value"""
        self.assertEqual(self.email_notification.get_template_id(), 1)

    def test_get_extra_headers(self):
        """Test ``get_extra_headers`` returns correct data structure"""
        self.assertEqual(
            self.email_notification.get_extra_headers(), {
                'Filters': {
                    'templates': {
                        'settings': {
                            'enable': 1,
                            'template_id': 1
                        }
                    }
                },
                'Subs': {}
            }
        )

    def test_convert_context_variables(self):
        """Test ``convert_context_variables`` converts ``dict`` to sendgrid's
         format"""
        email_notification = SendgridTemplateEmailNotification(
            context_variables={'key': 'value'})
        email_notification._to_emails = ['test']
        email_notification._bcc = ['test']
        self.assertEqual(
            email_notification._convert_context_variables(), {
                'key': ['value', 'value']
            }
        )
