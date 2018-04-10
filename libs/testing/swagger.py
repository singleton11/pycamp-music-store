import os
import pprint

from django.conf import settings
from django.test import TestCase, tag

from bravado.client import SwaggerClient
from bravado.exception import HTTPBadRequest
from bravado.swagger_model import load_file, load_url
from bravado_core.schema import collapsed_properties

from .django_client import DjangoClient


def get_swagger_client():
    """Shortcut function to init swagger client.

    Takes file path from django setting and initialize swagger client with
    custom DjangoClient
    """
    path = settings.TEST_SWAGGER_SPEC_FILE

    # check is path URL or path to local file
    if os.path.exists(path):
        conf_loader = load_file
    else:
        conf_loader = load_url

    try:
        swagger_data = conf_loader(path)
    except Exception:
        msg = 'Cannot load swagger file from "{}"'.format(path)
        raise AssertionError(msg) from None
    config = {
        'also_return_response': True,
    }
    return SwaggerClient.from_spec(
        swagger_data,
        config=config,
        http_client=DjangoClient(),
    )


# init swagger client here to not load spec for every test case
try:
    swagger_client = get_swagger_client()
except Exception:
    swagger_client = None


@tag('swagger')
class BaseSwaggerSpecTestCase(TestCase):
    """Base test case for checking Swagger speca in project

    This test can be used for testing methods got from Swagger spec.
    Its methods check that:

      * responses of methods produce data for all properties defined
        in the spec;
      * responses do not produce extra properties, which were not defined
        in the spec;
      * responses produce data in proper format and types defined in the spec.

    You can use ``assertResponseDataIsValid`` for checking response data

    Attributes:
        token (str): authorization token if you already have it
        token_format (str): format of authorization token

    """
    token = None
    token_format = 'token {token.key}'

    @classmethod
    def setUpClass(cls):
        """Check for correct swagger client initialization.

        Made in `setUpClass` so whole TestCase will fail if swagger client was
        not initialized
        """
        error_msg = 'Cannot load swagger file from "{}"'.format(
            settings.TEST_SWAGGER_SPEC_FILE
        )
        assert swagger_client, error_msg
        cls.swagger_client = swagger_client
        super().setUpClass()

    @property
    def swagger_spec(self):
        """Returns swagger spec from client"""
        return self.swagger_client.swagger_spec

    @property
    def swagger_models(self):
        """Models from swagger spec

        Returns:
            tuple: classes of models from swagger spec
        """
        return tuple(self.swagger_spec.definitions.values())

    def is_model(self, instance):
        """Checks whether item is swagger model

        Args:
            instance (object): object to check

        Returns:
            bool: True if object is swagger model
        """
        return type(instance) in self.swagger_models

    def login(self, **login_data):
        """This method perform login via API method

        It just gets the authorization token using the specified API method
        (auth:AuthLogin in this case)

        If request was successful, method updates ``token`` attribute.

        Args:
            login_data (dict): data for authorization

        Examples:
            self.login(email='myaddr@host.com', password='p@$$w0rd')

        """
        params = {
            'LoginData': login_data
        }
        data, _ = self.request('auth:AuthLogin', params)
        self.token = self.token_format.format(token=data)

    def clear_token(self):
        """Clears token value
        """
        self.token = None

    def api_method(self, method_label):
        """Returns callable for API method

        Args:
            method_label (str): name of method. It can be send in two ways:
                * 'resource_name:method_name'
                * 'method_name' (method name should be uniq)

        Returns:
            bravado.client.CallableOperation: corresponding method of API
        """
        if ':' in method_label:
            resource_name, method_name = method_label.split(':')

        else:
            resource_name, method_name = '', method_label

        method = None

        if resource_name:
            resource = getattr(self.swagger_client, resource_name)
            method = getattr(resource, method_name, None)

        else:
            for resource_name in dir(self.swagger_client):
                resource = getattr(self.swagger_client, resource_name, None)

                if not resource or not hasattr(resource, method_name):
                    continue

                method = getattr(resource, method_name)
                break

        if not method:
            raise AttributeError('Method {0} not defined'.format(method_label))

        return method

    def request(self, method_label, params, opts=None):
        """Shortcut for performing request using API method with params

        Args:
            method_label (str): label of method (see ``api_method`` docs)
            params (dict): dictionary with the method's parameters
            opts (dict): additional request options
                see: http://bravado.readthedocs.io/en/latest/configuration.html
                #per-request-configuration

        Examples:

            params = {'conference': str(self.conference.id)}
            data, result = self.request('getMyProfile', params)

            params = {'LoginData': {'email': email, 'password': password}}
            data, result = self.request('Auth:AuthLogin', params)

        Returns:
            tuple: tuple with data (index 0) and response result (index 1)
                The first item contains just data of response
                The second item contains full information (including the first
                item)
        """
        method = self.api_method(method_label)
        params = params.copy()

        if method.operation.security_specs and self.token:
            params['Authorization'] = self.token

        return method(**params).result()

    @staticmethod
    def _make_assertion_message(message, obj, prop, json_data, **kwargs):
        """Shortcut for making messages for assertion

        Args:
            message (str): template of message
            obj (object): instance of swagger-model
            prop (str|list): name(-s) of property(-es)
            json_data (object): json representation of obj
            **kwargs: some additional data

        Returns:
            str: assertion message
        """
        template_parts = ('', message, 'Model: {model}', 'JSON: {json}')
        template = '\n'.join(template_parts)
        return template.format(prop=prop,
                               model=type(obj),
                               json=pprint.pformat(json_data),
                               **kwargs)

    def _assertModelIsValid(self, obj, json_obj):
        """Asserts that object is valid against its swagger spec

        Args:
            obj (object): instance of model data

        """
        # we do not validate non-models objects
        if not self.is_model(obj):
            return

        _msg = self._make_assertion_message

        unexpected_props = obj._additional_props
        msg = _msg("Properties '{prop}' were not defined in spec",
                   obj=obj, prop=unexpected_props, json_data=json_obj)
        self.assertSetEqual(unexpected_props, set(), msg=msg)
        self._assertAttributesIsValid(obj, json_obj)

    def _assertAttributesIsValid(self, obj, json_obj):
        """Assert that attributes of instance of swagger-model is valid

        Args:
            obj (object): instance of swagger-model
            json_obj (object): json representation of instance from response

        """
        _msg = self._make_assertion_message

        for attr_name in dir(obj):
            definition_spec = self._get_swagger_model_spec(obj)
            if definition_spec[attr_name].get('x-nullable', False):
                continue
            attr_value = getattr(obj, attr_name)

            msg = _msg("Response doesn't provide data for '{prop}'",
                       obj=obj, prop=attr_name, json_data=json_obj)
            self.assertIn(attr_name, list(json_obj), msg=msg)

            json_value = json_obj[attr_name]

            if isinstance(attr_value, list):

                msg = _msg("Lenghts of property '{prop}' are differ",
                           obj=obj, prop=attr_name, json_data=json_obj)
                self.assertEqual(len(attr_value), len(json_value or []),
                                 msg=msg)

                for item, json_item in zip(attr_value, json_value):
                    self._assertModelIsValid(item, json_item)

            elif self.is_model(attr_value):
                self._assertModelIsValid(attr_value, json_value)

    def _get_swagger_model_spec(self, obj):
        """Retieve raw json swagger spec for ``obj``"""
        all_definitions = self.swagger_spec.spec_dict['definitions']
        definition_name = obj.__class__.__name__
        defintion_raw = all_definitions[definition_name]
        return collapsed_properties(defintion_raw, self.swagger_spec)

    def assertResponseDataIsValid(self, response_data, response_result):
        """Assert that response from self.request is valid against swagger spec

        Args:
            response_data (object): response data to check

        Examples:

            params = {}
            data, result = self.request('getConferencesList', params)
            self.assertResponseDataIsValid(data)

        """
        if not response_data:
            return

        json_data = response_result.json()
        if isinstance(response_data, list):
            for item, json_item in zip(response_data, json_data):
                self._assertModelIsValid(item, json_item)
        else:
            self._assertModelIsValid(response_data, json_data)

    def assertResponseIsValid(self, method_label, params, opts=None):
        """Asserts that response of method with params is valid

        Args:
            method_label (str): label of method (see ``api_method`` docs)
            params (dict): dictionary with the method's parameters
            opts (dict): additional request options
                see: http://bravado.readthedocs.io/en/latest/configuration.html
                #per-request-configuration

        """
        response = self.request(method_label, params, opts)
        self.assertResponseDataIsValid(*response)

    def assertBadRequest(self, method_label, params, opts=None):
        """Ensure that request with passed params will return BadRequest

        Args:
            method_label (str): label of method (see ``api_method`` docs)
            params (dict): dictionary with the method's parameters
            opts (dict): additional request options
                see: http://bravado.readthedocs.io/en/latest/configuration.html
                #per-request-configuration

        """
        try:
            self.request(method_label, params, opts)
        except HTTPBadRequest as bravado_exception:
            # ensure that swagger spec contain correct error spec
            if bravado_exception.swagger_result is None:
                self.fail(
                    'Swagger spec for bad request is not properly defined'
                )
        except Exception:
            self.fail('Unexpected result for bad request')
