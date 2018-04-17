from apps.music_store.utils import handle_uploaded_archive, NestedDirectoryError
from unittest import mock
from django.test import TestCase


class TestUploadZIPArchive(TestCase):
    """"""
    @classmethod
    def setUpTestData(cls):
        cls.nested_archive = 'decorator_task.zip'
        cls.no_album_archive = 'texts.zip'

    @mock.patch('zipfile.is_zipfile', return_value=False)
    def test_upload_not_a_zip_file(self, mock_iszip):

        with self.assertRaises(TypeError):
            handle_uploaded_archive(self.nested_archive)

    @mock.patch('apps.music_store.utils.add_track', side_effect=NestedDirectoryError)
    def test_upload_archive_with_nested_directories(self, mock_handle):

        with self.assertRaises(NestedDirectoryError):
            handle_uploaded_archive(self.no_album_archive)


