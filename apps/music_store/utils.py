import zipfile
from random import randrange
from .models import Album, Track


class NestedDirectoryError(Exception):
    """When album directory contains nested directory."""


class AlbumUploader:
    """"""
    author_title_delimiter = ' - '

    def _get_audio_data(self, audio_name):
        """"""
        if audio_name.count(self.author_title_delimiter):
            author, title = audio_name.split(self.author_title_delimiter)
            return author, title
        return None, audio_name

    def _get_data_from_filename(self, filename):
        """Get author, album title and track title from filename"""
        data = dict()
        # track file in album directory
        if filename.count('/') == 1:
            album, track = filename.split('/')
            album_author, album_title = self._get_audio_data(album)
            track_author, track_title = self._get_audio_data(track)

            data['author'] = album_author
            data['album'] = album_title
            data['track'] = track_title
        # track without album
        else:
            data['album'] = None
            track_author, track_title = self._get_audio_data(filename)
            data['author'] = track_author
            data['track'] = track_title
        return data

    def _add_track(self, track_file, track_data):
        """Create Track from file if it does not exist.

        If album does not exist, create it. Otherwise update existing album.

        """
        track_title = track_data['track']
        album_title = track_data['album']
        author = track_data['author']

        if not author:
            author = 'Unknown artist'
        # check existence of album
        if album_title and not Album.objects.filter(author=author,
                                                    title=album_title).exists():
            album = Album.objects.create(author=author,
                                         title=album_title,
                                         price=randrange(100, 200))
        else:
            album = Album.objects.filter(author=author,
                                         title=album_title).first()
        # check duplicates of track
        if not Track.objects.filter(author=author, title=track_title).exists():
            content = track_file.readlines()
            Track.objects.create(
                author=author,
                title=track_title,
                album=album,
                full_version=content,
                free_version='',
                price=randrange(5, 10),
            )

    def no_nested_folders_in_albums(self, zip_file):
        """"""
        for info in zip_file.infolist():
            # album directory contains nested directory
            if info.filename.count('/') > 1:
                return False
        return True

    def zip_album_handler(self, zip_file):
        """"""
        for info in zip_file.infolist():
            track_data = self._get_data_from_filename(info.filename)
            track_file = zip_file.open(info.filename)
            self._add_track(track_file, track_data)
            track_file.close()


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
        if not album_uploader.no_nested_folders_in_albums(zf):
            raise NestedDirectoryError(f'{zf.name} contains nested directory!')
        album_uploader.zip_album_handler(zf)
