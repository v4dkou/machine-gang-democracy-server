from urllib import parse
from base64 import b64encode

from rest_framework.pagination import CursorPagination


class MaxIdPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    cursor_query_param = 'maxid'

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded
