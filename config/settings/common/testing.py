"""Config that define tests-specific settings.
Also set `TESTING` attribute for `django.conf.settings`
"""
import sys

TESTING = False
TEST_RUNNER = 'libs.testing.CustomTestRunner'

if len(sys.argv) >= 2 and sys.argv[1] in ['test', 'jenkins']:
    TESTING = True


# applications which used for testing
TESTING_APPS = tuple()

if TESTING:
    from .installed_apps import INSTALLED_APPS
    INSTALLED_APPS += TESTING_APPS
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
