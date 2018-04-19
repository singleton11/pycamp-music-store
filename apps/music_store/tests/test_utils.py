from ..utils import (
    handle_uploaded_archive,
    NestedDirectoryError,
    AlbumUploader,
)
from ..models import Track, Album
from unittest.mock import patch, Mock, mock_open
from django.test import TestCase
from faker import Faker


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


class TestUploadZIPArchive(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.archive = Mock()
        cls.handler = AlbumUploader()
        cls.track_title = fake.word()
        cls.album_title = fake.word()
        cls.author = fake.word()

    @patch('zipfile.is_zipfile', return_value=False)
    def test_not_a_zip_file(self, mock_iszip):
        """Test for opening not a zip file"""

        with self.assertRaises(TypeError):
            handle_uploaded_archive(self.archive)

    @patch('zipfile.is_zipfile', return_value=True)
    @patch.object(AlbumUploader, 'is_no_folders_in_albums', return_value=False)
    def test_archive_with_nested_directories(self, mock_add_track, mock_iszip):
        """Test for nested directories in album folder"""
        with patch('zipfile.ZipFile') as mock:
            with self.assertRaises(NestedDirectoryError):
                handle_uploaded_archive(self.archive)

    def test_data_from_filename_with_only_track_title(self):
        filename = f'{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            ('Unknown artist', None, self.track_title,)
        )

    def test_data_from_filename_with_author_and_track_title(self):
        filename = f'{self.author} - {self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            (self.author, None, self.track_title,)
        )

    def test_data_from_filename_with_album_and_track_title(self):
        filename = f'{self.album_title}/{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            ('Unknown artist', self.album_title, self.track_title,)
        )

    def test_data_from_filename_full_info(self):
        filename = f'{self.author} - {self.album_title}/{self.track_title}'
        self.assertEqual(
            self.handler._get_data_from_filename(filename),
            (self.author, self.album_title, self.track_title,)
        )

    def test_zip_album_handler(self):
        self.archive.infolist = mock_infolist
        self.archive.open = mock_openfile

        self.handler.zip_album_handler(self.archive)

        self.assertEqual(Track.objects.all().count(), 4)
        self.assertEqual(Album.objects.all().count(), 2)
