import itertools
import os

from django.conf import settings
from django.template import context_processors

from .paths import BASE_DIR


def debug(request):
    """
    In the case we work through docker's shared network we should add its IP
    inside INTERNAL_IPS and then pass processing to django's own debug function
    defined inside context_processors
    """
    if settings.DEBUG:
        # automatically add REMOTE_IP which is docker's network gateway
        # into settings.INTERNAL_IPS
        remote = request.META['REMOTE_ADDR']
        if remote not in settings.INTERNAL_IPS:
            settings.INTERNAL_IPS.append(remote)

    return context_processors.debug(request)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'config.settings.common.templates.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
