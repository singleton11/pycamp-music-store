"""This module contain classes for using Django's test client for swagger.


Main class - ``DjangoClient`` which is used as `http_client` for bravado
(https://github.com/Yelp/bravado/) - python client library for Swagger 2.0
services

Bravado contains only ``RequestsClient`` and ``FidoClient`` for making
requests to API defined in swagger files. But ``RequestsClient`` requires
a real HTTP-server for responses, so testing swagger files require
``django.test.LiveServerTestCase`` and this requests are extremely slow.

``DjangoClient`` uses ``django.test.Client`` class for making requests and
tests run faster.
"""

from django.test.client import MULTIPART_CONTENT, Client
from django.utils.http import urlencode

from inflection import underscore

from bravado.http_client import HttpClient
from bravado.http_future import FutureAdapter, HttpFuture
from bravado_core.response import IncomingResponse


class DjangoClient(HttpClient):
    """Fake http client based on ``django.test.Client``.

    Main purpose of this class - prepare
    `bravado.http_future.HttpFuture` instance. This class used for making
    asnyc requests (but we do not implement this).
    """

    def request(self, request_params, operation=None, response_callbacks=None,
                also_return_response=False):
        """Method that should return `bravado_core.http_future.HttpFuture`.

        This method is called from bravado core.

        Args:
            request_params(dict): complete request data. e.g. url, method,
                headers, body, params, connect_timeout, timeout, etc.
            operation(bravado_core.operation.Operation): operation that this
                http request is for. Defaults to None - in which case, we're
                obviously just retrieving a Swagger Spec.
            response_callbacks(list): List of callables to post-process the
                incoming response. Expects args incoming_response and
                operation.
            also_return_response: Consult the constructor documentation for
                `bravado.http_future.HttpFuture`.

        Returns:
            `bravado_core.http_future.HttpFuture` - HTTP Future object
        """
        if operation is None:
            raise TypeError('Do not use this adapter to retrieve spec')

        # prepare instance of Future Adapter which will be called later from
        # HttpFuture object
        requests_future = DjangoFutureAdapter(
            request_params, operation, also_return_response
        )

        # Instantiate HttpFuture with passed args and adapter
        return HttpFuture(
            requests_future,
            DjangoResponseAdapter,
            operation,
            response_callbacks,
            also_return_response
        )


class DjangoFutureAdapter(FutureAdapter):
    """Mimics a `concurrent.futures.Future` for the purposes of making
    HTTP calls with the Django client in a future-y sort of way.

    Attributes:
        request_params, operation, also_return_response - parameters passed
        from ``DjangoClient.request`` (see it's docstring)

    ``request_params` dict can contain following keys:
    headers, data, params, files, url, method.

    Main purpose for this class - prepare params from ``request_params`` and
    use it to call proper method of ``django.test.Client``
    """

    def __init__(self, request_params, operation, also_return_response):
        """Prepare args to call ``django.test.client``."""
        self.client = Client()

        self.request_params = request_params
        self.operation = operation
        self.also_return_response = also_return_response

        self.path = self.prepare_path(
            request_params['url'],
            request_params['params']
        )
        self.method = request_params['method']
        self.secure = self.path.startswith('https')
        content_type = request_params['headers'].pop('Content-Type', None)
        self.headers = self.prepare_headers(request_params['headers'])

        # prepare request data
        self.data = request_params.get('data', {})
        for param_name, data in request_params.get('files', []):
            f_name, f_content = data
            self.data[param_name] = f_content

        if self.method == 'POST':
            self.content_type = content_type or MULTIPART_CONTENT
            self.data = self.client._encode_data(self.data, self.content_type)
        else:
            self.content_type = content_type or 'application/octet-stream'

    def prepare_headers(self, headers_raw):
        """Convert headers names to acceptable by Django client.

        Example:
            Authorization -> HTTP_AUTHORIZATION
        """
        headers = {}
        for name, value in headers_raw.items():
            new_name = 'HTTP_{}'.format(underscore(name).upper())
            headers[new_name] = value
        return headers

    def prepare_path(self, path, params):
        """Add GET-params to path
        """
        return '{base}?{params}'.format(
            base=path,
            params=urlencode(params, doseq=True)
        )

    def result(self, timeout=None):
        """Blocking call to wait for API response.

        This is main method that make request to django and should return
        raw response.

        Args:
            timeout(int): timeout for async call. Not used
        """
        return self.client.generic(
            method=self.method,
            path=self.path,
            data=self.data,
            content_type=self.content_type,
            secure=self.secure,
            **self.headers
        )


class DjangoResponseAdapter(IncomingResponse):
    """Wraps a django response object to provide a uniform interface
    to the response innards.

    Attributes:
        django_response: response from django test client
    """

    def __init__(self, django_response):
        self.django_response = django_response

    @property
    def status_code(self):
        return self.django_response.status_code

    @property
    def text(self):
        return self.django_response.text

    @property
    def headers(self):
        return self.django_response.headers

    @property
    def reason(self):
        return self.django_response.reason_phrase

    def json(self):
        return self.django_response.json()
