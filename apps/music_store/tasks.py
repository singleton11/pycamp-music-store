from random import randint
import time
import zipfile
import os

from celery import shared_task, states, current_task
from .utils import handle_uploaded_archive, AlbumUnpacker
from django.core.files.storage import default_storage


@shared_task
def get_albums_from_zip(zip_filename):
    """Get albums and tracks from ZIP file.

    Args:
        zip_filename (str): filename of uploaded zip_file.

    """
    time_to_sleep = randint(5, 15)

    time.sleep(time_to_sleep)
    zip_file = default_storage.open(zip_filename)
    try:
        albums_count, tracks_count = handle_uploaded_archive(zip_file)
    except Exception as e:
        # return error message for avoid break the request
        return str(e)

    time.sleep(time_to_sleep)
    return f'{albums_count} albums and {tracks_count} have been added.'


@shared_task
def get_tracks_from_zip(zip_filename):
    """Get albums and tracks from ZIP file.
    Report status of getting tracks.

    Args:
        zip_filename (str): filename of uploaded zip_file.

    """
    time_to_sleep = randint(5, 15)

    time.sleep(time_to_sleep)
    zip_file = default_storage.open(zip_filename)
    unpacker = AlbumUnpacker()

    if not unpacker.is_valid_uploaded_music_archive(zip_file):
        current_task.update_state(
            state=states.FAILURE,
            meta='INVALID ARCHIVE'
        )
    else:
        with zipfile.ZipFile(zip_file) as zf:
            for info in zf.infolist():
                track_data = unpacker._get_data_from_filename(info.filename)
                if track_data.track:
                    current_task.update_state(
                        state='UNPACKING',
                        meta=f'{track_data} is unpacking'
                    )
                    track_file = zf.open(info.filename)
                    unpacker._add_track(track_file, track_data)
                time.sleep(time_to_sleep)

    return f'{unpacker.added_albums_count} albums added. ' \
           f'{unpacker.added_tracks_count} tracks added'




