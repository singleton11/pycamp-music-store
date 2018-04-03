from fabric.api import local
from fabric.colors import green

from . import common, is_local_python

##############################################################################
# Run commands
##############################################################################

__all__ = ['docker_compose_run',
           'docker_compose_up',
           'docker_compose_start',
           'run_web',
           'run_web_python',
           'run_local_python',
           'run_python'
           ]


def docker_compose_up(command):
    """Up ``command`` using docker-compose

    docker-compose up <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    print(green(common.message(
        "Up {} containers ".format(command))))
    return local(' '.join(['docker-compose', 'up', command]))


def docker_compose_start(command):
    """Start ``command`` using docker-compose

    docker-compose start <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    print(green(common.message(
        "Start {} containers ".format(command))))
    return local(' '.join(['docker-compose', 'start', command]))


def docker_compose_run(command):
    """Run ``command`` using docker-compose

    docker-compose run <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    return local(' '.join(['docker-compose', 'run', '--rm', command]))


def docker_compose_exec(service, command):
    """Run ``exec`` using docker-compose

    docker-compose run <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    return local(' '.join(['docker-compose', 'exec', service, command]))


def run_web(command):
    """Run command in``web`` container.

    docker-compose run --rm web <command>
    """
    return docker_compose_run(' '.join(['--service-ports', 'web', command]))


def run_web_python(command):
    return run_web(' '.join(['python3', command]))


def run_local_python(command):
    """Run command using local python interpreter"""
    return local(' '.join(['python3', command]))


if is_local_python:
    run_python = run_local_python
else:
    run_python = run_web_python
