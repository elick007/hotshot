from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from hotshot.base.restbase import CustomResponse


class LargeResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        code = 1
        msg = 'success'
        if not data:
            code = 0
            msg = 'Data Not Found'
            response_data = data
        else:
            response_data = {'videoList': data, 'nextLink': self.get_next_link()}
        return CustomResponse(data=response_data, code=code, msg=msg, status=status.HTTP_200_OK)
