from django.test import TestCase

from ..strings import convert, hide_except_last


class StiringTestCase(TestCase):
    """Test case for strings.py"""
    def test_hide_except_last(self):
        """Test ``hide_except_last`` function, should return the same string in
        which all symbols replaces by '*' except last ``num`` which is 4 by
        default"""
        self.assertEqual(hide_except_last('TestTestTest'), '********Test')

    def test_convert_str(self):
        """Test ``convert`` function, should return result of funciton which
        applied to ``item`` stirng arg"""
        self.assertEqual(convert('TestTest', hide_except_last), '****Test')

    def test_convert_list(self):
        """Test ``convert``, should return result of applying function to
        ``item`` list arg"""
        self.assertEqual(
            convert(['TestTest', 'TestTest'], hide_except_last),
            ['****Test', '****Test']
        )
