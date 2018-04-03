from fabric.colors import green

from . import common, start


def init():
    """Create virtualhost in rabbitmq and grants permissions
    """
    print(green(common.message(
        "Initial configuration for rabbitmq")))
    start.docker_compose_exec(
        'rabbitmq', 'rabbitmqctl add_vhost "music_store_exercise-development"')  # noqa
    start.docker_compose_exec(
        'rabbitmq', 'rabbitmqctl add_user music_store_exercise_user manager')  # noqa
    start.docker_compose_exec(
        'rabbitmq',
        'rabbitmqctl set_permissions -p "music_store_exercise-development" music_store_exercise_user ".*" ".*" ".*"')  # noqa
