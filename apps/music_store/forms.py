import zipfile
import re
from .models import Album, Track
from tempfile import NamedTemporaryFile
from django.forms import forms


class AlbumUploadArchiveForm(forms.Form):
    """Form for upload archive"""
    file = forms.FileField()


class NestedDirectoryError(Exception):
    """When album directory contains nested directory

    """


def split_file_name(audio_name):
    """Check if name of album or track is valid to format:
         Author_name - album_or_track_title

    """
    if re.match(r'.+s/*-s/*.+', audio_name):
        author, title = re.split(r's/*-s/*', audio_name)
    # if no author name in filename
    else:
        author, title = None, audio_name
    return author, title


def get_data_from_filename(filename):
    """Get author, album title and track title from filename"""
    data = {
        'author': '',
        'album': '',
        'track': '',
    }
    # album directory contains nested directory
    if filename.count('/') > 1:
        raise NestedDirectoryError(
            f'{filename} contains nested directory!'
        )
    # track file in album directory
    if filename.count('/') == 1:
        album, track = filename.split('/')
        album_author, album_title = split_file_name(album)
        track_author, track_title = split_file_name(filename)

        data['author'] = album_author
        data['album'] = album_title
        data['track'] = track_title
    # track without album
    else:
        data['album'] = None
        track_author, track_title = split_file_name(filename)
        data['author'] = track_author
        data['track'] = track_title

    return data


def add_track(track_file):
    """Create Track from file if it does not exist.

    If album does not exist, create it. Otherwise update existing album.

    """
    track_data = get_data_from_filename(track_file.name)
    track = track_data['track']
    album = track_data['album']
    author = track_data['author']

    if not author:
        author = 'Unknown artist'

    # check existence of album
    if album and not Album.objects.filter(author=author, album=album).exists():
        album = Album.objects.create(author=author, title=album, price=100)

    # check duplicates of track
    if not Track.objects.filter(author=author, title=track).exists():
        with open(track_file) as tf:
            content = tf.readlines()
            Track.objects.create(
                author=author,
                title=track,
                album=album,
                full_version=content,
                free_version='free_version',
                price=10,
            )


def handle_uploaded_archive(archive_file):
    """Handler of zip archive with albums and tracks.

    ZIP archive can contain only single files of tracks and album directories
    with track files. Directories CAN NOT contain nested directories.

    """
    with NamedTemporaryFile() as tmp_archive:
        # put archive into temporary file tmp_file
        for chunk in archive_file.chunks():
            tmp_archive.write(chunk)

        if not zipfile.is_zipfile(tmp_archive):
            raise TypeError('It is not a ZIP archive!')

        # process names
        with zipfile.ZipFile(archive_file) as zf:
            for info in zf.infolist():
                track_file = tmp_archive.open(info.filename)

                try:
                    add_track(track_file)
                except NestedDirectoryError as e:
                    raise e

                track_file.close()
