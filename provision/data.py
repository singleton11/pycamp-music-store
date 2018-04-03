import os

from fabric.api import task
from fabric.colors import green, red
from fabric.contrib import console

from . import common, django

##############################################################################
# Data generation for database
##############################################################################

__all__ = [
    'sync_from_remote',
    'load_fixtures']


@task
def sync_from_remote(environment='development'):
    """
    Sync data from development DB -> Local DB (remote sync)

    This should connect to development server environment and sync remote
    DB with local DB completely overwriting local data. This is helpful
    for new developers joining to project during its maintenance phase and
    allows easier sync of the data to local DB. Local DB's data will be
    overwritten
    """
    # TODO: Dmitry to implement once I get additional info from our
    # devops team
    print(green(common.message(
        "Sync from remote database")))
    if console.confirm(
            "Do you want to sync with {} DB?\n"
            "This will overwrite your local DB data".format(environment)):
        print(red('No Implementation! Please implement this accordingly'))
        return False


def load_fixtures(*args):
    """Load fixtures to database

    Examples:
        # load specified fixtures
        fab data.load_fixtures:users.json,clients.json

    """
    print(green(common.message(
        "Load fixtures")))
    fixture_folder = '.dev/fixtures'
    order_file = os.path.join(fixture_folder, '.fixtures-order')
    fixtures = []
    if args:
        fixtures = args
    else:
        with open(order_file) as order:
            fixtures = [os.path.join(fixture_folder, fixture)
                        for fixture in map(str.strip, order)
                        if fixture and not fixture.startswith('#')]
    for fixture in fixtures:
        django.manage(' '.join(['loaddata', fixture]))
