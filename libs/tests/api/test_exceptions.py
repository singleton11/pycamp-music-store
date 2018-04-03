import unittest

from django.core.exceptions import PermissionDenied as CorePermissionDenied
from django.http import Http404
from django.test import TestCase

from rest_framework.exceptions import (
    APIException,
    NotFound,
    PermissionDenied,
    ValidationError,
)

from faker import Faker

from libs.api.exceptions import CustomAPIException, custom_exception_handler

fake = Faker()


class CustomCodeError(CustomAPIException):
    status_code = fake.numerify()
    code = fake.word()
    message = fake.sentence()


class DefaultCodeError(APIException):
    status_code = fake.numerify()
    default_code = fake.word()
    default_detail = fake.sentence()


class TestCustomExceptionHandler(TestCase):
    """Tests for ``custom_exception_handler`` method."""

    def test_validation_error_for_list(self):
        """Test ``custom_exception_handler`` for ValidationError (list).

        If ValidationError detail is a list, method will add to detail the
        message from list.

        """
        error_msg = fake.word()
        exception = ValidationError(error_msg)
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], 'validation_error')
        self.assertEqual(response.data['detail'], error_msg)

    @unittest.skip("FIX")
    def test_custom_code_error(self):
        """Test ``custom_exception_handler`` for ``CustomAPIException``.

        All exceptions that are inherited from ``CustomAPIException`` already
        have proper detail format.

        """
        exception = CustomCodeError()
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], exception.code)
        self.assertEqual(response.data['detail'], exception.message)

    @unittest.skip("FIX")
    def test_default_code_error(self):
        """Test ``custom_exception_handler`` for ``APIException``.

        All exceptions that are inherited from ``APIException`` (e.g. any
        native DRF exception like ``NotAuthenticated``) and not
        ``ValidationError`` are parsed using 'default_code' and
        'default_detail'.

        """
        exception = DefaultCodeError()
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], exception.default_code)
        self.assertEqual(response.data['detail'], exception.default_detail)

    def test_non_field_error(self):
        """Test ``custom_exception_handler`` for non field errors."""
        error_msg = fake.sentence()
        exception = ValidationError({'non_field_errors': [error_msg]})
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], 'validation_error')
        self.assertEqual(response.data['detail'], error_msg)

    def test_field_error(self):
        """Test ``custom_exception_handler`` for field errors."""
        field_name = fake.word()
        field_error = [fake.sentence()]
        exception = ValidationError({field_name: field_error})
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], 'validation_error')
        self.assertEqual(
            response.data['validation_errors'][0]['field'], field_name
        )
        self.assertEqual(
            response.data['validation_errors'][0]['errors'], field_error
        )

    def test_non_field_and_field_error(self):
        """Test ``custom_exception_handler`` for non field and field errors."""
        non_field_error_msg = fake.sentence()
        field_name = fake.word()
        field_error = [fake.sentence()]

        exception = ValidationError({
            'non_field_errors': [non_field_error_msg],
            field_name: field_error
        })

        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], 'validation_error')
        self.assertEqual(response.data['detail'], non_field_error_msg)
        self.assertEqual(
            response.data['validation_errors'][0]['field'], field_name
        )
        self.assertEqual(
            response.data['validation_errors'][0]['errors'], field_error
        )

    def test_http_404(self):
        """Test ``custom_exception_handler`` for HTTP 404 error."""
        exception = Http404()
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], NotFound.default_code)
        self.assertEqual(response.data['detail'], NotFound.default_detail)

    def test_permission_denied(self):
        """Test ``custom_exception_handler`` for ``PermissionDenied``."""
        exception = CorePermissionDenied()
        response = custom_exception_handler(exception)
        self.assertEqual(response.data['code'], PermissionDenied.default_code)
        self.assertEqual(
            response.data['detail'], PermissionDenied.default_detail
        )


class TestCustomAPIException(TestCase):
    """Tests for ``CustomAPIException`` class."""

    def test_custom_error(self):
        """Test for exception class, inherited from ``CustomAPIException``."""
        exc = CustomCodeError()
        self.assertEqual(exc.status_code, exc.status_code)
        self.assertEqual(exc.default_code, exc.code)
        self.assertEqual(exc.detail, exc.message)

    def test_default_error(self):
        """Test for default ``CustomAPIException`` exception class."""
        exc = CustomAPIException()
        self.assertEqual(exc.status_code, APIException().status_code)
        self.assertEqual(exc.default_code, 'custom_api_exception')
        self.assertEqual(exc.detail, APIException().detail)
