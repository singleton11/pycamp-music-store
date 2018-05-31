import zipfile
from unittest.mock import Mock, mock_open

from django.test import TestCase

from faker import Faker

from ..models import Album, Track
from apps.music_store.utils.upload import AlbumUnpacker, NestedFolderError


def mock_infolist(obj):
    """Mock of Zipfile.infolist() method."""
    fake = Faker()
    return [
        fake.file_name(),
        f'{fake.word()} - {fake.word()}.txt',
        f'{fake.word()}/{fake.word()}.txt',
        f'{fake.word()} - {fake.word()}/{fake.word()}.txt',
    ]


def mock_unpacker(is_zip=True, is_no_folders=True):
    """Mock AlbumUnpacker methods and attributes for tests.

    Args:
        is_zip (bool): to mock behaviour if zip archive given or not
        is_no_folders (bool): to mock behaviour if zip archive contain nested
            folders in album folders or not

    """
    zipfile.ZipFile = Mock()
    zipfile.is_zipfile = Mock(return_value=is_zip)
    zipfile.ZipFile.infolist = mock_infolist
    AlbumUnpacker.nested_check = Mock(return_value=is_no_folders)
    AlbumUnpacker._get_track_list = mock_infolist


class TestUploadZIPArchive(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()
        cls.track_title = cls.fake.word()
        cls.album_title = cls.fake.word()
        cls.author = cls.fake.word()

        # mock AlbumUnpacker
        mock_unpacker()
        cls.archive = Mock()
        cls.unpacker = AlbumUnpacker(cls.archive)
        cls.unpacker.zip_file.open = mock_open(
            read_data=cls.fake.sentence(30)
        )

    def test_unpack_not_a_zip_file(self):
        """Test for opening not a zip file"""
        mock_unpacker(is_zip=False)
        with self.assertRaises(TypeError):
            AlbumUnpacker(self.archive)

    def test_unpack_archive_with_nested_directories(self):
        """Test for nested directories in album folder"""
        mock_unpacker(is_no_folders=False)

        with self.assertRaises(NestedFolderError):
            AlbumUnpacker(self.archive)

    # tests for getting correct data from filenames in archive
    def test_data_from_filename_with_only_track_title(self):
        filename = f'{self.track_title}'
        self.assertEqual(
            self.unpacker._get_track_info(filename),
            ('Unknown artist', None, self.track_title,)
        )

    def test_data_from_filename_with_author_and_track_title(self):
        filename = f'{self.author} - {self.track_title}'
        self.assertEqual(
            self.unpacker._get_track_info(filename),
            (self.author, None, self.track_title,)
        )

    def test_data_from_filename_with_album_and_track_title(self):
        filename = f'{self.album_title}/{self.track_title}'
        self.assertEqual(
            self.unpacker._get_track_info(filename),
            ('Unknown artist', self.album_title, self.track_title,)
        )

    def test_data_from_filename_full_info(self):
        filename = f'{self.author} - {self.album_title}/{self.track_title}'
        self.assertEqual(
            self.unpacker._get_track_info(filename),
            (self.author, self.album_title, self.track_title,)
        )

    def test_unpack_track_handler(self):
        """Test unpacking tracks from zip archive"""
        for track_filename in self.unpacker.track_list:
            self.unpacker.track_handler(track_filename)

        self.assertEqual(Track.objects.all().count(), 4)
        self.assertEqual(Album.objects.all().count(), 2)
