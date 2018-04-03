from fabric.api import local, task
from fabric.colors import green

from . import common, is_local_python, start

##############################################################################
# Linters
##############################################################################

__all__ = ['pep8', 'js', 'sass', 'all']


def isort(path=''):
    """Sorts python imports by the specified path"""
    local('isort {path}'.format(path=path))


def isort_fix(path=None, print_msg=True):
    """Command to fix imports formatting."""
    if print_msg:
        print('Running imports fix\n')
    return isort(path) if path else isort('-rc -y --skip .venv')


@task
def pep8():
    """Check PEP8 errors
    """
    print(green(common.message(
        "Linters: PEP8 running")))

    execute = local if is_local_python else start.run_web
    isort_fix()
    return execute('flake8 --config=.flake8 apps libs')


@task
def sass():
    """Check SASS errors
    """
    print(green(common.message(
        "Linters: SASS running")))
    return local('npm run lint-sass')


@task
def js():
    """Check JS errors
    """
    print(green(common.message(
        "Linters: JS running")))
    local("npm run lint-js")


@task
def all():
    """Run all linters (JS, SASS, PEP8)
    """
    js()
    sass()
    pep8()
