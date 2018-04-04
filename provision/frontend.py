import os
import time

from fabric.api import local, task
from fabric.colors import green

from . import common

##############################################################################
# Frontend ops
##############################################################################


def init():
    """Install node packages needed for frontend development
    """
    local('npm install')


@task
def build():
    """Build assets with brunch
    """
    local('npm run build')


@task
def watch():
    """Watch assets to be modified and rebuild with brunch
    """
    local('npm run start')
