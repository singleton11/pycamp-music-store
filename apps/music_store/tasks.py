from random import randint
import time

from celery import shared_task
from .utils import handle_uploaded_archive
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
