from collections import namedtuple

from config.celery import app

from uuid import uuid4


# Data about celery task for further display task status and result
TaskInfo = namedtuple('TaskInfo', ['id', 'status', 'result'])


def get_celery_task_status_info(task_id):
    """Return celery task status information as a dict"""
    task_data = app.AsyncResult(task_id)

    task_info = TaskInfo(task_data.task_id, task_data.state, task_data.result)

    # if task returned exception, result = error_message
    if isinstance(task_info.result, Exception):
        task_info.result = str(task_info.result)

    return task_info


def unique_track_name(instance, filename):
    """Rename file of track full version on upload"""
    ext = filename.split('.')[-1]
    return f'{uuid4()}.{ext}'


def rename_free_version(instance, filename):
    """Rename file of track free version on upload.

    New filename has format %full_version_name%_free.ext

    """
    filename, ext = instance.full_version.name.split('.')
    return f'{filename}_free.{ext}'
