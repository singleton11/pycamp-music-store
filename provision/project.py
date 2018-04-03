import os
import time

from fabric.api import local, task
from fabric.colors import green

from . import (
    common,
    data,
    django,
    docker,
    frontend,
    is_local_python,
    rabbitmq,
    system,
    tests,
)

##############################################################################
# Build project locally
##############################################################################

__all__ = ['build',
           'init',
           'install_dependencies',
           'compiledeps',
           'compiledeps_rebuild'
           ]


def copylocal(force_update=True):
    """Copy local settings from template

    Args:
        force_update(bool): rewrite file if exists or not
    """
    local_settings = 'config/settings/local.py'
    local_template = 'config/settings/local.py.template'

    if force_update or not os.path.isfile(local_settings):
        local(' '.join(['cp', local_template, local_settings]))


@task
def build(container=None):
    """Build python environ"""
    if is_local_python:
        install_reqs()
    else:
        print(green(common.message(
            "Rebuilding docker {} container".format(container)))
        )

        cmd = 'docker-compose build'
        if container:
            cmd = '{} {}'.format(cmd, container)
        local(cmd)


@task
def init(clean=False):
    """Buld project from scratch
    """

    print(green(common.message(
        "Initial assembly of all dependencies")))
    system.hooks()
    system.gitmessage()
    compiledeps()
    install_dependencies()
    if clean:
        docker.clear()
    copylocal()

    build()
    django.makemigrations()
    django.migrate()
    django.createsuperuser()
    rabbitmq.init()

    tests.run()

    # if this is first start of the project
    # then the following line will generate exception
    # informing first developer to make factories
    try:
        success = data.sync_from_remote()
        if not success:
            data.load_fixtures()
    except NotImplementedError:
        print(
            "Awesome, almost everything is Done! \n"
            "You're the first developer - pls generate factories \n"
            "for test data and setup development environment")

    print(green(common.message(
        "Type `MUSIC_STORE_EXERCISE_ENVIRONMENT=local fab django.run` to start web app")))


##############################################################################
# Manage dependencies
##############################################################################

def install_dependencies():
    """Install shell/cli dependencies

    Define your dependencies here, for example
    local('sudo npm -g install ngrok')
    """
    local('pip install --upgrade setuptools pip')


def install_reqs(env='development'):
    """Install local development requirements"""
    print(green(common.message(
        "Install pip dependencies")))
    local('pip install -r requirements/{env}.txt'.format(env=env))


@task
def compiledeps(u=False):
    """Compile pip dependencies"""
    print(green(common.message(
        "Compile pip dependencies")))
    upgrade = '-U' if u else ''
    in_files = [
        'requirements/development.in',
        'requirements/production.in',
    ]
    for in_file in in_files:
        local(
            'pip-compile {in_file} {upgrade}'.format(
                in_file=in_file,
                upgrade=upgrade)
        )


@task
def compiledeps_rebuild(container='web'):
    """Recompile dependencies and re-build docker containers
    web container
    """
    compiledeps()
    build(container)
