import time
from random import randint

from django.core.files.storage import default_storage

from celery import current_task, shared_task

from .utils import AlbumUnpacker


# External state for celery task of getting tracks from zip archive
UNPACKING_STATE = 'UNPACKING'


@shared_task
def get_tracks_from_zip(zip_filename):
    """Get albums and tracks from ZIP file.
    Report status of getting tracks.

    Args:
        zip_filename (str): filename of uploaded zip_file.

    """
    # delay to simulate unpacking takes a long time
    time_to_sleep = randint(3, 6)

    with default_storage.open(zip_filename) as zip_file:

        unpacker = AlbumUnpacker(zip_file)

        for track_filename in unpacker.track_list:
            current_task.update_state(
                state=UNPACKING_STATE,
                meta=f'{track_filename} is unpacking...'
            )

            # simulate unpacking takes a long time
            time.sleep(time_to_sleep)

            unpacker.track_handler(track_filename)

        return (
            f'{unpacker.added_albums_count} albums added. '
            f'{unpacker.added_tracks_count} tracks added'
        )
