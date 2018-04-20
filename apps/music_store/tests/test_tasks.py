from unittest.mock import Mock, mock_open, patch

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings

from faker import Faker

from ..tasks import get_albums_from_zip
from ..utils import AlbumUploader

fake = Faker()
mock_openfile = mock_open(read_data=fake.sentence(30))


def mock_infolist():
    """Mock of Zipfile.infolist() method."""
    files = [
        Mock(filename=fake.file_name()),
        Mock(filename=f'{fake.word()} - {fake.word()}.txt'),
        Mock(filename=f'{fake.word()}/{fake.word()}.txt'),
        Mock(filename=f'{fake.word()} - {fake.word()}/{fake.word()}.txt'),
    ]
    return files


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestGetAlbumsFromZipTask(TestCase):
    """Tests for celery task gets albums and tracks from zip file"""
    @classmethod
    def setUpTestData(cls):
        cls.file = default_storage.save('testfile', ContentFile('new content'))
        cls.archive = Mock()
        cls.handler = AlbumUploader()

    def test_upload_not_zip_file(self):
        result = get_albums_from_zip.delay(self.archive)
        self.assertTrue(result.failed())

    @patch.object(AlbumUploader, 'is_no_folders_in_albums', return_value=False)
    def test_upload_incorrect_zip_file(self, mock_nested_folders):
        result = get_albums_from_zip.delay(self.archive)
        self.assertTrue(result.failed())

    @patch('zipfile.is_zipfile', return_value=True)
    def test_upload_correct_zip_file(self, mock_iszip):

        with patch('zipfile.ZipFile') as mock:

            default_storage.open = mock_open(read_data=fake.sentence(30))
            self.archive.infolist = mock_infolist

            result = get_albums_from_zip.delay(self.archive)
            self.assertTrue(result.successful())
