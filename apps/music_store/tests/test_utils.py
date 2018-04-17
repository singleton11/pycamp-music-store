from apps.music_store.utils import handle_uploaded_archive, NestedDirectoryError
from unittest.mock import patch, Mock, mock_open
from django.test import TestCase
from faker import Faker
import builtins
from zipfile import ZipFile


fake = Faker()
mock_openfile = mock_open(read_data=fake.sentence(20))


def mock_infolist(albums=False, nested=False):
    """Mock of Zipfile.infolist() method

    Args:
        albums (bool): if mock zip provide album directories
        nested (bool): of any album dir contain nested dir

    """
    files = [
        Mock(filename=fake.file_name()),
        Mock(filename=f'{fake.word} - {fake.file_name()}'),
    ]
    if albums:
        files.extend(
            [
                Mock(filename=f'{fake.word} - {fake.word}/{fake.file_name()}'),
                Mock(filename=f'{fake.word}/{fake.file_name()}'),
            ]
        )
    if nested:
        files.append(
            Mock(filename=fake.file_path(2))
        )

    return files


class TestUploadZIPArchive(TestCase):
    """"""

    @classmethod
    def setUpTestData(cls):
        cls.archive = './apps/music_store/tests/test.zip'

    @patch('zipfile.is_zipfile', return_value=False)
    def test_not_a_zip_file(self, mock_iszip):
        """Test for opening not a zip file"""

        with self.assertRaises(TypeError):
            handle_uploaded_archive(self.archive)

    @patch('apps.music_store.utils.add_track', side_effect=NestedDirectoryError)
    def test_archive_with_nested_directories(self, mock_add_track):
        """Test for nested directories in album folder"""

        with self.assertRaises(NestedDirectoryError):
            handle_uploaded_archive(self.archive)


