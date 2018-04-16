# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
    'debug_toolbar',
    'cacheops',
    'corsheaders',
    'storages',
    'taggit',
    'imagekit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'opbeat.contrib.django',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'rest_framework_swagger',
    'taggit_serializer',
    'rest_auth',
    'rest_auth.registration',
    'push_notifications',
    'django_celery_beat',
)

LOCAL_APPS = (
    'libs',
    'apps.users',
    'apps.music_store',
)

INSTALLED_APPS += LOCAL_APPS
