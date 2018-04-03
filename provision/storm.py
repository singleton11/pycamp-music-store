from fabric.api import local, settings, task
from fabric.colors import green

from . import common, docker

##############################################################################
# Storm start stop commands
##############################################################################


__all__ = ['run']


@task
def run(**kwargs):
    """Run storm related services and containers"""

    print(green(common.message(
        "Start storm containers ")))

    docker.run_containers(
        'zookeeper',
        'kafka',
        'nimbus',
        'supervisor',
        'ui',
        **kwargs)
