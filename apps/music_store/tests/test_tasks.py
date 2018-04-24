from unittest.mock import Mock, mock_open

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings

from faker import Faker

from ..tasks import get_tracks_from_zip
from ..utils import AlbumUnpacker
from .test_utils import mock_unpacker


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestGetAlbumsFromZipTask(TestCase):
    """Tests for celery task gets albums and tracks from zip file"""
    @classmethod
    def setUpTestData(cls):
        cls.file = default_storage.save('testfile', ContentFile('new content'))

    def test_upload_not_zip_file(self):
        result = get_tracks_from_zip.delay(self.file)
        self.assertTrue(result.failed())

    def test_upload_incorrect_zip_file(self):
        mock_unpacker(is_no_folders=False)

        result = get_tracks_from_zip.delay(self.file)
        self.assertTrue(result.failed())

    def test_upload_correct_zip_file(self):
        # mock AlbumUnpacker instance
        fake = Faker()
        mock_unpacker()
        archive = Mock()
        unpacker = AlbumUnpacker(archive)
        unpacker.zip_file.open = mock_open(
            read_data=fake.sentence(30)
        )

        default_storage.open = mock_open(read_data=fake.sentence(30))

        result = get_tracks_from_zip.delay(archive)
        print(result.result)
        self.assertTrue(result.successful())
