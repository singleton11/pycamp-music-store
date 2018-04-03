"""Tests for ``libs.utils`` module
"""
from django.test import TestCase

from libs.utils import get_attr


class TestGetAttrFunction(TestCase):
    """Tests for ``libs.utils.get_attr`` function
    """

    def setUp(self):

        class Author(object):
            def __init__(self, uid):
                self.id = uid

        class Book(object):
            def __init__(self, author):
                self.author = author

        self.book = Book(author=Author(200))

    def test_get_attr_with_empty_string(self):
        """Tests that on empty path function raises ``AttributeError``"""
        with self.assertRaises(AttributeError, msg=None):
            get_attr(self.book, '')

    def test_get_attr_with_existed_attr(self):
        """Tests that function works property for existed path"""
        actual_value = get_attr(self.book, 'author.id')
        self.assertIs(actual_value, self.book.author.id)

    def test_returning_default_on_not_existed_attr(self):
        """Tests that function returns default value for not existed path
        """
        actual_value = get_attr(self.book, 'author.not_existed',
                                default='DEFAULT')
        self.assertEqual(actual_value, 'DEFAULT')

    def test_raise_attribute_error_on_not_existed_attr(self):
        """Tests that ``AttributeError`` is raised for not existed path
        """
        with self.assertRaises(AttributeError):
            get_attr(self.book, 'author.not_existed')
