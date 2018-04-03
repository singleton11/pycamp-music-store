from base64 import b64encode

from django.conf import settings

from rest_framework.pagination import CursorPagination, urlparse

from constance import config

__all__ = ('OrderByModifiedCursorPagination',)


class OrderByModifiedCursorPagination(CursorPagination):
    """Provides cursor pagination base on ``created`` field and
    next/prev links as cursor value.

    When you use this pagination you will get something like this:

    {
        "next": "cD0y...QTAw",  # cursor value for next page
        "previous": "cj0x...0EwMA",  # cursor value for previous page
        "results": [...]  # page content
    }

    """
    offset_cutoff = None

    def get_page_size(self, request):
        """Returns page size for pagination process

        If ``pageSize`` in request params then return that
        If ENVIRONMENT is ``development`` then return value from admin's
        constance
        Another way return self.page_size

        Returns:
            int: page size
        """
        # try get page size from request params
        query_page_size = request.GET.get('pageSize', None)
        if query_page_size:
            try:
                return int(query_page_size)
            except ValueError:
                pass

        # if site in development mode then return value from admin's constance
        if settings.ENVIRONMENT == 'development':
            return config.PAGE_SIZE

        return self.page_size

    def encode_cursor(self, cursor):
        """Encodes cursor instance to use in params

        Overrides the parent method to return a cursor value instead
        URL containing cursor.

        This method used in parent ``get_paginated_response`` method
        to provide correct 'next' and 'previous' values.

        Args:
            cursor (Cursor):  instance of cursor to encode

        Returns:
            str: encoded cursor
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        return b64encode(querystring.encode('ascii')).decode('ascii')


class OrderByIDCursorPagination(OrderByModifiedCursorPagination):
    """Order by ID cursor pagination.

    Custom cursor paginated for objects without ``created`` field -- ordering
    by ID.

    """
    ordering = 'id'
