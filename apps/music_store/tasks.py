from celery import shared_task
from .utils import handle_uploaded_archive
from django.core.files.storage import default_storage


@shared_task
def get_albums_from_zip(zip_filename):
    """Get albums and tracks from ZIP file.

    Args:
        zip_filename (str): filename of uploaded zip_file.

    """
    zip_file = default_storage.open(zip_filename)
    albums_count, tracks_count = handle_uploaded_archive(zip_file)
    return f'{albums_count} albums and {tracks_count} have been added.'
