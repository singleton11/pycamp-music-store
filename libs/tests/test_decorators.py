from django.test import TestCase

from libs.decorators import related_properties


class TestRelatedPropertiesDecorator(TestCase):
    """Test for ``related_properties`` decorator"""
    def setUp(self):
        class Conference(object):
            # emulates django model
            uid = None

            def __init__(self, uid):
                self.uid = uid

        class Module(object):
            uid = None
            conference = None

            def __init__(self, uid, conference):
                self.uid = uid
                self.conference = conference

        self.conference = Conference(1)
        self.module = Module(2, self.conference)

    def test_properties(self):
        """Tests that required properties were added"""

        @related_properties(
            conference='module.conference',
            module_uid='module.uid',
            conference_uid='module.conference.uid',
        )
        class Event(object):
            uid = None
            module = None

            def __init__(self, uid, module):
                self.uid = uid
                self.module = module

        event = Event(3, self.module)

        self.assertEqual(event.conference, self.conference)
        self.assertEqual(event.module_uid, self.module.uid)
        self.assertEqual(event.conference_uid, self.conference.uid)

    def test_existing_property(self):
        """AssertationError should be raised because decorated class
        already has ``uid`` and ``module`` attributes
        """
        with self.assertRaises(AssertionError):

            @related_properties(uid='module.uid')
            class Event(object):

                uid = None
                module = None

                def __init__(self, uid, module):
                    self.uid = uid
                    self.module = module
