from app.settings import *

DEBUG = False
ENVIRONMENT = 'production'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'music_store_exercise_production',
        'USER': 'music_store_exercise_user',
        'PASSWORD': 'manager',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

ACCOUNT_EMAIL_VERIFICATION = 'none'


INSTALLED_APPS += (
    # other apps for production site
)
