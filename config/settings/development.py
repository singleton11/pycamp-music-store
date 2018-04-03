from .common import *

DEBUG = True
ENVIRONMENT = 'development'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '%DB_NAME%',
        'USER': '%DB_USER%',
        'PASSWORD': '%DB_PASSWORD%',
        'HOST': '%DB_HOST%',
        'PORT': '%DB_PORT%',
    }
}

INSTALLED_APPS += (
    'django_extensions',
)

# Stripe Configuration
# TODO: setup stripe params
# STRIPE_SECRET_KEY = 'sk_test_secret_key'
# STRIPE_PUBLIC_KEY = 'pk_test_public key'

# Django Storages S3
# TODO: setup AWS params
AWS_S3_ACCESS_KEY_ID = '%AWS_S3_ACCESS_KEY_ID%'
AWS_S3_SECRET_ACCESS_KEY = '%AWS_S3_SECRET_ACCESS_KEY%'
AWS_STORAGE_BUCKET_NAME = '%AWS_STORAGE_BUCKET_NAME%'
AWS_S3_ENDPOINT_URL = '%AWS_S3_ENDPOINT_URL%'

# If you wish to use AWS S3 storage simply comment or remove the line below
# In this case storage params are defined by config/settings/commons/storage.py
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# SendGrid
# TODO: setup sendgrid params
# SENDGRID_ID = 'sendgrid_id'
# SENDGRID_KEY = 'sendgrid_ley'
# SENDGRID_API_KEY = SENDGRID_KEY

# EMAIL Notification
# TODO: setup email params
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'user_name'
# EMAIL_HOST_PASSWORD = 'password'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '%EMAIL_HOST%'
EMAIL_HOST_USER = '%EMAIL_HOST_USER%'
EMAIL_HOST_PASSWORD = '%EMAIL_HOST_PASSWORD%'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# PUSH Notifications
# TODO: setup push notifications params
# PUSH_NOTIFICATIONS_SETTINGS = {
#     'GCM_API_KEY': 'AIzaSyAej0Dw2Mcy2ppj_JpSwgY25yn6jpnKgp4',
#     'APNS_CERTIFICATE': BASE_DIR + '/app/certs/crtdev/cert.pem',
# }




# LOGGER
OPBEAT = {
    'ORGANIZATION_ID': '%OPBEAT_ORG_ID%',
    'APP_ID': '%OPBEAT_APP_ID%',
    'SECRET_TOKEN': '%OPBEAT_TOKEN%',
    'DEBUG': True,
}


# Swagger
# TODO: update me
TEST_SWAGGER_SPEC_FILE = None


# Configuration for django-jenkins
INSTALLED_APPS += (
    'django_jenkins', 
    'django_pdb',
)
JENKINS_TASKS = (
    'django_jenkins.tasks.run_flake8', 
)
JENKINS_TEST_RUNNER = 'libs.testing.JenkinsCustomTestRunner'

# Specify apps for django-jenkins
PROJECT_APPS = LOCAL_APPS


# Celery config
CELERY_TASK_DEFAULT_QUEUE = '%CELERY_QUEUE%'.format(
    ENVIRONMENT=ENVIRONMENT)
CELERY_BROKER = ('amqp://%RABBITMQ_USER%:%RABBITMQ_HOST%@%'
                 'RABBITMQ_HOST%/%CELERY_QUEUE%').format(
                     ENVIRONMENT=ENVIRONMENT)
CELERY_BACKEND = 'redis://%REDIS_HOST%/%REDIS_DB%'


# Cache ops
CACHEOPS_REDIS = {
    'host': '%REDIS_HOST%', # redis-server is on same machine
    'port': 6379,           # default redis port
    'db': 1,                # SELECT non-default redis database
                            # using separate redis db or redis instance
                            # is highly recommended
    'socket_timeout': 3     # connection timeout in seconds, optional
}


