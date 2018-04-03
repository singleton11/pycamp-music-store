from fabric.api import local, task
from fabric.colors import green

from . import common, django, is_local_python, start

##############################################################################
# Test commands
##############################################################################

__all__ = ['run',
           'run_clear',
           'run_fast',
           'coverage']


@task
def run(path='', p='--keepdb --parallel --failfast'):
    """Run django tests with ``extra`` args for ``p`` tests.

    `p` means `params` - extra args for tests

    manage.py test <extra>
    """
    print(green(common.message(
        "Tests {} running ".format(path))))
    django.manage(' '.join(['test', path, p]))


@task
def run_clear(path=''):
    """Alias for tests without `keepdb` flag"""
    run(path=path, p='--noinput --parallel --failfast')


@task
def run_fast(path=''):
    """Run django tests as fast as possible.

    No migrations, keep DB, parallel.

    manage.py test --keepdb --failfast --parallel <path>
    """
    run(path=path, p='--keepdb --failfast --parallel')


@task
def coverage(extra='--keepdb --failfast'):
    """Generate and display test-coverage"""
    print(green(common.message(
        "Calculate and display code coverage")))
    execute = local if is_local_python else start.run_web

    execute(' '.join(['coverage run manage.py test', extra]))
    execute('coverage html')
    local('xdg-open htmlcov/index.html & sleep 3')
