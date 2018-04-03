import operator
import os
import uuid
from datetime import datetime
from shutil import make_archive
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import mktime

import pytz
from PIL import Image


def get_random_filename(filename):
    """Get random filename.

    Generation random filename that contains unique identifier and
    filename extension like: ``photo.jpg``.

    If extension is too long (we had issue with that), replace it with
    UUID too

    Args:
        filename (str): Name of file.

    Returns:
        new_filename (str): ``9841422d-c041-45a5-b7b3-467179f4f127.ext``.

    """
    path = str(uuid.uuid4())
    ext = os.path.splitext(filename)[1]
    if len(ext) > 15:
        ext = str(uuid.uuid4())

    return ''.join([path, ext.lower()])


def calculate_age(birthdate):
    diff = datetime.now() - birthdate
    return diff.days // 365


def struct_time_to_timezoned(struct_time):
    """Convert ``struct_time`` object to timezoned ``datetime.datetime`` to
    pass to django ``DateTimeField`` with timezone
    """
    timestamp = mktime(struct_time)
    utc_date = datetime.utcfromtimestamp(timestamp)
    timezoned = utc_date.replace(tzinfo=pytz.utc)
    return timezoned


def get_attr(obj, attr_path, **kwargs):
    """Returns attribute of object, defined with in dot-path

    Examples:
        obj = Book(**kwargs)
        get_attr(obj, 'book.author.id', raise_attr_error=True)
        # returns obj.book.author.id

    Args:
        obj (object): object to process
        attr_path (str): path to attribute (Example: 'book.author.id')
        default (object): default value to return if ``raise_attr_error``
            is False
        raise_attr_error (bool): if True AttriubuteError will be raised if
            attribute does not exists

    Returns:
        object: attribute's value
    """
    _getattr = operator.attrgetter(attr_path)

    try:
        return _getattr(obj)
    except AttributeError:
        if 'default' in kwargs:
            return kwargs['default']
        raise


def to_tuple(obj):
    if isinstance(obj, (tuple, list, set)):
        return tuple(obj)
    else:
        return obj,


def get_file_extension(url):
    """Method to extract file extension from path/URL.

    Args:
        url (str): Path to the file

    Returns:
        String: extension of the file

    Example:
        'dir/subdir/file.ext' -> 'ext'

    """
    return os.path.splitext(url)[1][1:]


def get_file_size(file_field):
    """Returns size of a given file

    Args:
        file_field(file field) - instance of Django `models.FileField`

    Returns:
        int - size of a given file or 0
    """
    if not file_field:
        return 0

    try:
        return file_field.size
    except FileNotFoundError:
        return 0


class NewImage(object):
    """Context manager to create temporary image file.

    Example:
        with NewImage() as img:
            self.image = img

    """

    def __init__(self, width=500, height=500, ext='PNG', color='green',
                 prefix=None):
        self.width = width
        self.height = height
        self.color = color
        self.ext = ext
        self.prefix = prefix

    def __enter__(self):
        image = Image.new('RGB', (self.width, self.height), self.color)
        self.tmp_file = NamedTemporaryFile(
            delete=False,
            suffix='.{0}'.format(self.ext.lower()),
            prefix=self.prefix,
        )
        image.save(self.tmp_file.name, self.ext)
        return self.tmp_file

    def __exit__(self, *args):
        os.unlink(self.tmp_file.name)


class ZipArchive(object):
    """Context manager to create temporary zip archive with files.

    Structure of files and directories in archive:
        some_file.doc (if `file_without_folder` is True)
        /some_folder
            some_music_file.mp3
            some_image_file.png

    """

    def __init__(self, file_without_folder=False, file_with_invalid_ext=False):
        self.file_without_folder = file_without_folder
        self.file_with_invalid_ext = file_with_invalid_ext

    def __enter__(self):
        self.tmp_dir = TemporaryDirectory()
        self.tmp_subdir = TemporaryDirectory(dir=self.tmp_dir.name)

        self.tmp_zip = NamedTemporaryFile()
        self.tmp_file = NamedTemporaryFile(
            dir=self.tmp_subdir.name, suffix='.png')
        self.another_tmp_file = NamedTemporaryFile(
            dir=self.tmp_subdir.name, suffix='.mp3')

        # create file without folder
        if self.file_without_folder:
            self.tmp_file_without_parent_dir = NamedTemporaryFile(
                dir=self.tmp_dir.name,
                suffix='.mp3'
            )

        if self.file_with_invalid_ext:
            self.tmp_file_with_invalid_ext = NamedTemporaryFile(
                dir=self.tmp_subdir.name,
                suffix='.undefined'
            )

        self.image = Image.new('RGB', (1280, 720), 'green')
        self.image.save(self.tmp_file.name, 'PNG')

        self.zip_file = make_archive(self.tmp_zip.name, 'zip',
                                     self.tmp_dir.name)

        return {
            'tmp_zip': self.tmp_zip,
            'tmp_dir': self.tmp_dir,
            'tmp_file': self.tmp_file,
            'tmp_subdir': self.tmp_subdir,
            'zip_file': self.zip_file,
        }

    def __exit__(self, *args):
        self.tmp_file.close()
        self.another_tmp_file.close()

        if self.file_without_folder:
            self.tmp_file_without_parent_dir.close()

        if self.file_with_invalid_ext:
            self.tmp_file_with_invalid_ext.close()

        self.tmp_subdir.cleanup()
        self.tmp_dir.cleanup()
        return True


def get_object_fullname(obj):
    """Get fully qualified class name of an object in Python.

    May be used to dump object's class to string and later use to restore it
    using `import_string`.

    WARNING: simplest implementation used, may not work in some cases
    """
    return '.'.join([obj.__module__ + "." + obj.__class__.__name__])


def get_class_fullname(klass):
    """Get fully qualified class name of an class in Python.
    """
    return '.'.join([klass.__module__ + "." + klass.__name__])
