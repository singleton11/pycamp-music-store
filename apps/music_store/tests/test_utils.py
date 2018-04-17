from apps.music_store.utils import (
    handle_uploaded_archive,
    NestedDirectoryError,
    AlbumUploader,
)
from apps.music_store.models import Track, Album
from unittest.mock import patch, Mock, mock_open
from django.test import TestCase
from faker import Faker
from zipfile import ZipFile


fake = Faker()
mock_openfile = mock_open(read_data=fake.sentence(30))


def mock_infolist():
    """Mock of Zipfile.infolist() method.

    """
    files = [
        Mock(filename=fake.file_name()),
        Mock(filename=f'{fake.word()} - {fake.file_name()}'),
        Mock(filename=f'{fake.word()}/{fake.file_name()}'),
        Mock(filename=f'{fake.word()} - {fake.word()}/{fake.file_name()}'),
    ]
    return files


class TestUploadZIPArchive(TestCase):
    """"""

    @classmethod
    def setUpTestData(cls):
        cls.archive = './apps/music_store/tests/test.zip'
        cls.handler = AlbumUploader()
        cls.track_title = fake.word()
        cls.album_title = fake.word()
        cls.author = fake.word()

    @patch('zipfile.is_zipfile', return_value=False)
    def test_not_a_zip_file(self, mock_iszip):
        """Test for opening not a zip file"""

        with self.assertRaises(TypeError):
            handle_uploaded_archive(self.archive)

    @patch.object(AlbumUploader, 'no_nested_folders_in_albums', return_value=False)
    def test_archive_with_nested_directories(self, mock_add_track):
        """Test for nested directories in album folder"""

        with self.assertRaises(NestedDirectoryError):
            handle_uploaded_archive(self.archive)

    def test_data_from_filename_filename_with_only_track_title(self):
        filename = f'{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            {
                'author': None,
                'album': None,
                'track': self.track_title
            }
        )

    def test_data_from_filename_filename_with_author_and_track_title(self):
        filename = f'{self.author} - {self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            {
                'author': self.author,
                'album': None,
                'track': self.track_title
            }
        )

    def test_data_from_filename_filename_with_album_and_track_title(self):
        filename = f'{self.album_title}/{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            {
                'author': None,
                'album': self.album_title,
                'track': self.track_title
            }
        )

    def test_data_from_filename_filename_full_info(self):
        filename = f'{self.author} - {self.album_title}/{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            {
                'author': self.author,
                'album': self.album_title,
                'track': self.track_title
            }
        )

    @patch.object(ZipFile, 'infolist()', mock_infolist)
    @patch('builtins.open', mock_openfile)
    def test_zip_album_handler(self):
        self.handler.zip_album_handler(self.archive)

        self.assertEqual(
            Track.objects.all().count(),
            4
        )

        self.assertEqual(
            Album.objects.all().count(),
            2
        )


