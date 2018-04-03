import configparser

from fabric.api import env

__all__ = ['project_interpreter']

INTERPRETER_WEB = 'web'
INTERPRETER_LOCAL = 'local'

# read config
# config should be saved in file with name '.fabric'
# Format:
# ## .fabric
# [Project]
# interpreter = local

config = configparser.ConfigParser({'interpreter': INTERPRETER_WEB})
config.read('.fabric')

project_interpreter = INTERPRETER_WEB

if config.has_section('Project'):
    project_interpreter = config.get('Project', 'interpreter')

is_local_python = (project_interpreter == INTERPRETER_LOCAL)

# globally change some Fabric variables
env.update({
    'colorize_errors': True
})
