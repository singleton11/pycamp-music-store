from fabric.api import local, settings
from fabric.colors import green

from . import common


class FabricNetworkException(Exception):
    """Docker networking exception

    Used to bypass fatal error of fabric cli execution
    in the case desired docker network is already created
    """
    pass

##############################################################################
# Containers start stop commands
##############################################################################


__all__ = [
    'run_containers',
    'stop_containers']


def run_containers(*containers, **kwargs):
    """Run containers
    """
    print(green(common.message(
        "Start {} containers ".format(containers))))
    local(' '.join(['docker-compose', 'up', '-d' if kwargs.get('d') else ''] +
                   list(containers)))


def stop_containers(*containers):
    """Stop containers
    """
    print(green(common.message(
        "Stopping {} containers ".format(containers))))
    local(' '.join(['docker-compose', 'stop'] + list(containers)))


##############################################################################
# Containers networking
##############################################################################

def create_network(network=None):
    """Create docker network
    """
    if not network:
        return None

    print(green(common.message(
        "Create {} network".format(network))))

    with settings(abort_exception=FabricNetworkException):
        try:
            local('docker network create {}'.format(network))
        except FabricNetworkException:
            pass
