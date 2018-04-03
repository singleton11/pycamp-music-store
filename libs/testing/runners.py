import os
from shutil import rmtree
from tempfile import mkdtemp

from django.conf import settings
from django.test.runner import DiscoverRunner

from django_jenkins.runner import CITestSuiteRunner
from opbeat import Client

__all__ = ('CustomTestRunner', 'JenkinsCustomTestRunner')


class TempMediaForTestsMixin(object):
    """Mixin for work with temporary media directory during Django tests

    It does 4 things:
    1. Change `DEFAULT_FILE_STORAGE` setting to
        'django.core.files.storage.FileSystemStorage' so you do not have to
        worry about redefining it manually for tests
    2. Create temporary directory for storing media files during tests
    3. Update settings.MEDIA_ROOT to point to temp directory
    3. Deletes temp dir after tests.
    """

    def setup_test_environment(self, **kwargs):
        """Extends default method to change settings and create temporary
        directory
        """
        super().setup_test_environment(**kwargs)
        self._temp_media = mkdtemp()

        settings._original_default_file_storage = settings.DEFAULT_FILE_STORAGE
        settings.DEFAULT_FILE_STORAGE = (
            'django.core.files.storage.FileSystemStorage'
        )
        settings._original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self._temp_media

    def teardown_test_environment(self, **kwargs):
        """Restore settings and delete temp media dir
        """
        super().teardown_test_environment()
        rmtree(self._temp_media)

        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root

        settings.DEFAULT_FILE_STORAGE = (
            settings._original_default_file_storage)
        del settings._original_default_file_storage


class DisableOpbeatMixin(object):
    """Errors and metrics should not be send during tests
    """

    def setup_test_environment(self, **kwargs):
        """Disable Opbeat sending messages """
        super().setup_test_environment(**kwargs)

        self.original_opbeat_disable_send = \
            os.environ.get('OPBEAT_DISABLE_SEND', 'false')
        os.environ['OPBEAT_DISABLE_SEND'] = 'true'

    def teardown_test_environment(self, **kwargs):
        """Restore settings """
        super().teardown_test_environment()

        os.environ['OPBEAT_DISABLE_SEND'] = self.original_opbeat_disable_send


class OpbeatMixin(DisableOpbeatMixin):
    """Mixin for handling messages for Opbeat"""

    def suite_result(self, suite, result, **kwargs):
        """Overrides default method `suite_result`

        Integrates Opbeat notifications for tests failures and errors during
        Jenkins buildings process

        We put info about tests failures and errors into Opbeat's traceback
        dict. This is HACK because there is suggested that traceback will
        contains frames only for one exception. But we put each tests failure
        info into separate frame inside one Opbeat's traceback. This is
        needed for showing info about tests failures and errors in formatted
        representations with syntax highlights

        """
        if self.original_opbeat_disable_send != 'true':
            opbeat_conf = getattr(settings, 'OPBEAT', {})

            if len(result.failures) + len(result.errors) and opbeat_conf:
                # initialize client instance for Opbeat
                client = Client(
                    organization_id=opbeat_conf['ORGANIZATION_ID'],
                    app_id=opbeat_conf['APP_ID'],
                    secret_token=opbeat_conf['SECRET_TOKEN']
                )

                extra = {
                    'failures': len(result.failures),
                    'errors': len(result.errors),
                }
                data = {
                    'stacktrace': {'frames': []}
                }

                # fill-in info about failures and errors into Opbeat traceback
                for test, traceback in result.failures + result.errors:
                    data['stacktrace']['frames'].append(
                        self._build_traceback_frame(test, traceback)
                    )

                data = self._set_opbeat_additional_info(data)

                # send message into Opbeat
                client.capture_message(
                    self._get_opbeat_message(result),
                    data=data,
                    extra=extra
                )

        return super().suite_result(suite, result, **kwargs)

    @staticmethod
    def _build_traceback_frame(test, traceback):
        """Build Opbeat's traceback dict for given `traceback` and `test`

        Args:
            test: instance of Django test's class (inherited from `TestCase`)
            traceback: string which represents traceback info about
                       test failure or error
        """
        test_module_path = test.id()
        test_path = test_module_path.replace('.', '/')

        # get test's class name and test item
        test_case, function = tuple(
            test_module_path.split('.')[-2:]
        )

        # remove empty lines from traceback
        lines = list(filter(None, traceback.split('\n')))

        traceback_info = {
            "abs_path": test_path,
            "filename": test_case,
            "function": function,
            "vars": {},
            "pre_context": lines[:-1],
            "context_line": lines[-1],
            "lineno": len(lines),
            "post_context": []
        }

        return traceback_info

    @staticmethod
    def _set_opbeat_additional_info(data):
        """Fill `url` and `culprit` in Opbeat dara param

            Args:
                data: Opbeat's data dict
        """
        jenkins_build_url = os.environ.get('BUILD_URL')

        # set url to failed build
        if jenkins_build_url:
            data['http'] = {
                'url': jenkins_build_url.replace('http', 'https')
            }

        data['culprit'] = 'Jenkins CI'

        return data

    @staticmethod
    def _get_opbeat_message(result):
        """Build message for Opbeat notification

            Args:
                result: result of tests executions
        """
        jenkins_build_id = os.environ.get('BUILD_ID')

        message = 'JENKINS [build {build_id} failed]: ' \
                  'There are {failures} errors and {errors} fails in tests'\
            .format(
                build_id='#{}'.format(
                    jenkins_build_id) if jenkins_build_id else '',
                failures=len(result.errors),
                errors=len(result.failures)
            )

        return message


class DisableCeleryMixin(object):
    """Mixin that set ``USE_CELERY`` setting to ``False``.

    This is out custom setting that is just bool var that used to check if
    something should be run with celery.
    """

    def setup_test_environment(self, **kwargs):
        """Extends default method to change settings"""
        super().setup_test_environment(**kwargs)

        settings._original_use_celery = settings.USE_CELERY
        settings.USE_CELERY = False

    def teardown_test_environment(self, **kwargs):
        """Restore settings"""
        super().teardown_test_environment()

        settings.USE_CELERY = settings._original_use_celery
        del settings._original_use_celery


class CustomTestRunner(
        TempMediaForTestsMixin,
        DisableCeleryMixin,
        DisableOpbeatMixin,
        DiscoverRunner
):
    pass


class JenkinsCustomTestRunner(
        TempMediaForTestsMixin,
        DisableCeleryMixin,
        OpbeatMixin,
        CITestSuiteRunner
):
    pass
