from fabric.api import local, task
from fabric.colors import green

from . import common, is_local_python

##############################################################################
# Mkdocs
##############################################################################

__all__ = ['sphinx']


##############################################################################
# Sphinx
##############################################################################

@task
def sphinx():
    """Run watchdog to autobuild sphinx documentation

    This command starts docker container with sphinx and you can see sphinx
    docs at http://127.0.0.1:8001

    Also when you edit docs, browser will automatically reload page after
    rebuild
    """
    print(green(common.message(
        "Starting sphinx")))

    if is_local_python:
        local('sphinx-autobuild docs .dev/sphinx-docs -H 0.0.0.0 -p 8001 '
              '-i ".git/*" ')
    else:
        local('docker-compose up sphinx')
