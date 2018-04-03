import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import yaml


def get_current_swagger_spec_version():
    """Returns current swagger spec version

    "Current swagger spec version" is the one that the API is considered to be
    compatible with. This function must be used to report the version
    currently supported by the API.

    This implementation gets the version from the swagger spec file that is
    referenced in ACTUAL_SWAGGER_SPEC_FILE setting.

    Returns:
        str: version of the swagger spec (e.g. 0.0.42)

    Raises:
        ImproperlyConfigured: if ACTUAL_SWAGGER_SPEC_FILE cannot be parsed

    """
    file_path = settings.ACTUAL_SWAGGER_SPEC_FILE

    try:
        return extract_swagger_spec_version_from_yaml_file(file_path)
    except ValueError as e:
        raise ImproperlyConfigured(
            'Cannot extract version from({0}): {1}'.format(file_path, e)
        ) from e


def extract_swagger_spec_version_from_yaml_file(file_path):
    """Function parses given swagger file to get its version.

    Args:
        file_path (str): Path to a local spec file

    Returns:
        String: version of swagger file (e.g. 0.0.42)

    Raises:
        ValueError: if given `file_path` is not accessible or somehow invalid

    """
    try:
        if os.path.exists(file_path):
            with open(file_path) as f:
                raw_spec = f.read()
        else:
            raise ValueError(
                'Unknown scheme or such local file does not exist'
            )
        spec = yaml.safe_load(raw_spec)
        return spec['info']['version']
    except Exception as e:
        raise ValueError('{0}'.format(e)) from e
