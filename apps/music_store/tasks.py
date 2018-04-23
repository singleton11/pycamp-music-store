from random import randint
import time

from celery import shared_task, current_task
from .utils import AlbumUnpacker
from django.core.files.storage import default_storage


@shared_task
def get_tracks_from_zip(zip_filename):
    """Get albums and tracks from ZIP file.
    Report status of getting tracks.

    Args:
        zip_filename (str): filename of uploaded zip_file.

    """
    time_to_sleep = randint(3, 6)

    time.sleep(time_to_sleep)
    with default_storage.open(zip_filename) as zip_file:

        try:
            unpacker = AlbumUnpacker(zip_file)
        except Exception as e:
            # return error message if problems with zip_archive
            return str(e)

        for track_filename in unpacker.track_list:
            current_task.update_state(
                state='UNPACKING',
                meta=f'{track_filename} is unpacking...'
            )
            unpacker.track_handler(track_filename)

            time.sleep(time_to_sleep)

        return f'{unpacker.added_albums_count} albums added. ' \
               f'{unpacker.added_tracks_count} tracks added'
