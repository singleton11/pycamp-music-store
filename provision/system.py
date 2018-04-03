from fabric.api import local, task
from fabric.colors import green

from . import common

##############################################################################
# System shortcuts
##############################################################################

__all__ = ['hooks', 'chown']


@task
def hooks():
    """Install git hooks

    Used during ``build``
    """
    print(green(common.message(
        "Deploy git hooks")))
    local('mkdir -p .git/hooks')
    local('cp .git-hooks/* .git/hooks/')


def chown():
    """Shortcut for owning apps dir by current user after some files were
    generated using docker-compose (migrations, new app, etc)
    """
    local('sudo chown ${USER}:${USER} -R apps')


def gitmessage():
    """Set default .gitmessage
    """
    print(green(common.message(
        "Deploy git commit message template")))
    local('echo "[commit]" >> .git/config')
    local('echo "  template = .gitmessage" >> .git/config')
