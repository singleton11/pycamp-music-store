from celery import shared_task
from .utils import handle_uploaded_archive


@shared_task
def get_albums_from_zip(zip_file):
    """"""
    handle_uploaded_archive(zip_file)
    return f'{zip_file.filename} processed'
