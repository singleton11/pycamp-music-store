import zipfile
from collections import namedtuple

from config.celery import app
from .models import Album, Track


class NestedDirectoryError(Exception):
    """When album directory contains nested directory."""


class AlbumUploader:
    """Class for uploading albums and tracks.

    Provide handlers to get albums and tracks from uploaded files,
    get album and track titles and author from file names
    and put them into database.

    """
    author_title_delimiter = ' - '

    def __init__(self):
        self.added_albums_count = 0
        self.added_tracks_count = 0

    def is_no_folders_in_albums(self, zip_file):
        """Check if album folders contain nested directories"""
        for info in zip_file.infolist():
            # album directory contains nested directory
            if not info.is_dir() and info.filename.count('/') > 1:
                return False
        return True

    def zip_album_handler(self, zip_file):
        """Handler to get Albums and Tracks from zip archive.

        zip archive must have following structure:

            track_file_1.ext
            track_file_2.ext
            album_folder_1/track_file_1.ext
            album_folder_1/track_file_2.ext
            album_folder_2/track_file_1.ext

        Track files in root directory have empty album field.
        Track files in album_folder have album corresponding to album_folder.

        Files and folders must have following format:
            'author - title' or 'title'

        Args:
            zip_file (ZipFile): archive with Tracks and Albums.

        """
        for info in zip_file.infolist():
            track_file = zip_file.open(info.filename)
            track_data = self._get_data_from_filename(info.filename)
            self._add_track(track_file, track_data)
            track_file.close()

        return self.added_albums_count, self.added_tracks_count

    def _add_track(self, track_file, track_data):
        """Create Track from file if it does not exist.

        If album does not exist, create it. Otherwise update existing album.

        """
        # check existence of album
        album = None
        if track_data.album:
            album, created = Album.objects.get_or_create(
                author=track_data.author,
                title=track_data.album,
                defaults={
                    'title': track_data.album,
                    'author': track_data.author
                }
            )
            if created:
                self.added_albums_count += 1

        # check duplicates of track
        if not Track.objects.filter(author=track_data.author,
                                    title=track_data.track).exists():
            content = track_file.read()
            Track.objects.create(
                author=track_data.author,
                title=track_data.track,
                album=album,
                full_version=content,
            )
            self.added_tracks_count += 1

    def _get_data_from_filename(self, filename):
        """Get author, album title and track title from filename"""
        track_data = namedtuple('TrackData', ['author', 'album', 'track'])

        # track file in album directory
        if filename.count('/') == 1:
            album, track = filename.split('/')
            album_author, album_title = self._get_audio_data(album)
            _, track_title = self._get_audio_data(track)
            return track_data(album_author, album_title, track_title)
        # track without album
        track_author, track_title = self._get_audio_data(filename)
        return track_data(track_author, None, track_title)

    def _get_audio_data(self, audio_name):
        """Get author and title values.

        Args:
            audio_name (str): Album or Track description in following format:
                'author_name - title' or 'title'

        Returns:
            (tuple): author(str) and title(str) if audio_name contain both
                or None and title(str) if audio_name contain only title

        """
        if audio_name.count(self.author_title_delimiter):
            author, title = audio_name.split(self.author_title_delimiter)
            return author, title
        return 'Unknown artist', audio_name


def handle_uploaded_archive(archive_file):
    """Handler of zip archive with albums and tracks.

    ZIP archive can contain only single files of tracks and album directories
    with track files. Directories CAN NOT contain nested directories.

    """
    if not zipfile.is_zipfile(archive_file):
        raise TypeError('It is not a ZIP archive!')

    album_uploader = AlbumUploader()

    # process names
    with zipfile.ZipFile(archive_file) as zf:
        if not album_uploader.is_no_folders_in_albums(zf):
            raise NestedDirectoryError(f'{zf.filename} has a nested folder!')
        return album_uploader.zip_album_handler(zf)
    return 0, 0


def get_celery_task_status_info(request, task_key):
    """Return celery task status information as a dict"""
    task_id = request.session.get(task_key)
    task_data = app.AsyncResult(task_id)

    task_dict = {
        'key': task_key,
        'id': task_data.task_id,
        'status': task_data.state,
        'result': task_data.result,
    }

    # if task returned exception, result = error_message
    if isinstance(task_dict['result'], Exception):
        task_dict['result'] = str(task_dict['result'])

    return task_dict