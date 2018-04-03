import os

from fabric.api import task
from fabric.colors import green, red

from . import common, start, system

##############################################################################
# Django commands and stuff
##############################################################################

__all__ = ['manage',
           'makemigrations',
           'migrate',
           'resetdb',
           'run',
           'shell',
           'dbshell'
           ]


@task
def manage(command):
    """Run ``manage.py`` command

    docker-compose run --rm web python3 manage.py <command>
    """
    return start.run_python(' '.join(['manage.py', command]))


@task
def makemigrations():
    """Run makemigrations command and chown created migrations
    """
    print(green(common.message(
        "Django: Make migrations")))
    manage('makemigrations')
    system.chown()


@task
def migrate():
    """Run ``migrate`` command"""
    print(green(common.message(
        "Django: Apply migrations")))
    manage('migrate')


@task
def resetdb():
    """Reset database to initial state (including test DB)"""
    print(green(common.message(
        "Reset database to its initial state")))
    manage('drop_test_database --noinput')
    manage('reset_db -c --noinput')
    makemigrations()
    migrate()
    createsuperuser()


def createsuperuser():
    """Create superuser
    """
    print(green(common.message(
        "Create superuser")))
    manage('createsuperuser')


@task
def run():
    """Run development web-server"""

    # start dependencies (so even in local mode this command
    # is working successfully
    # if you need more default services to be started define them
    # below, like celery, kafka etc.
    start.docker_compose_start('postgres redis rabbitmq')
    try:
        env = os.environ["MUSIC_STORE_EXERCISE_ENVIRONMENT"]  # noqa
    except KeyError:
        print(red(common.message(
            "Please set the environment variable "
            "MUSIC_STORE_EXERCISE_ENVIRONMENT, like=local")))
        exit(1)
    print(green(common.message(
        "Running web app")))
    start.run_python(
        "manage.py runserver_plus 0.0.0.0:8000  --reloader-type stat --pm")


@task
def shell(params=None):
    """Shortcut for manage.py shell_plus command

    Additional params available here:
        http://django-extensions.readthedocs.io/en/latest/shell_plus.html
    """
    print(green(common.message(
        "Entering Django Shell")))
    manage('shell_plus --ipython {}'.format(params or ""))


@task
def dbshell():
    """Open postgresql shell with credentials from either local or dev env"""
    print(green(common.message(
        "Entering DB shell")))
    manage('dbshell')
