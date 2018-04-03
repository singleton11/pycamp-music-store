import tempfile

from django.utils import timezone


def generate_file(size=1024):
    """Generates file with specified size

    It can be used in tests

    Args:
        size (int): size of file

    Returns:
        file: generated file
    """
    tmp_file = tempfile.NamedTemporaryFile()
    with open(tmp_file.name, 'wb') as out:
        out.write(b'x' * size)
    return tmp_file


def get_curr_time():
    """Helper function to get current server's time.

    Current server time used during model's sync (look for
    `sync_from` and `sync_to`).

    Used actively on uSummit
    """
    return str(timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
