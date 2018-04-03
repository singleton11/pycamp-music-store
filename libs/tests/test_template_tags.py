from unittest.mock import patch

from django.test import TestCase

from ..templatetags.active import activate_if_active


class MockRequest(object):
    """Class for create mock ``Request`` object which has ``get_full_path``
    method"""
    def get_full_path(self):
        """Always return 'test'"""
        return 'test'


class MockResolveMatch(object):
    """Class for create mock ``ResolveMatch`` objects which should have
    ``url_name`` attribute"""
    def __init__(self, url_name):
        self.url_name = url_name


class TemplateTagsTestCase(TestCase):
    @patch('django.core.urlresolvers.RegexURLResolver.resolve', return_value=MockResolveMatch('test'))
    def test_activate_if_active(self, resolve):
        """Test if ``resolve`` result match with arg (it means class 'active'
        should be placed on the tag)"""
        self.assertEqual(activate_if_active(MockRequest(), 'test'), 'active')

    @patch('django.core.urlresolvers.RegexURLResolver.resolve', return_value=MockResolveMatch('test1'))
    def test_activate_if_active_url_not_match(self, resolve):
        """Test if ``resolve`` result is not matched with arg (it means class
        'active' should not be placed on the tag)"""
        self.assertEqual(activate_if_active(MockRequest(), 'test'), '')
