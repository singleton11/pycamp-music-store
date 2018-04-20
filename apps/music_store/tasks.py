from celery import shared_task
from .utils import handle_uploaded_archive
from django.core.files.storage import default_storage


@shared_task
def get_albums_from_zip(zip_file):
    """Get albums and tracks from ZIP file.

    Args:
        zip_file (str): filename of uploaded zip_file.

    """
    zf = default_storage.open(zip_file)
    handle_uploaded_archive(zf)
    return f'{zip_file} processed'
