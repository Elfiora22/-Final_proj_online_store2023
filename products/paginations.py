from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil


class ProductPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        page = int(self.request.query_params.get(self.page_query_param, 1))
        pages = ceil(self.page.paginator.count / self.page_size)
        previeous_num_page = None
        next_num_page = None
        if page > 1:
            previeous_num_page = page - 1
        if pages > page:
             next_num_page = page + 1
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "next_num_page": next_num_page,
                "previous_num_page": previeous_num_page
            },
            "page": page,
            "pages": pages,
            "count": self.page.paginator.count,
            "result": data
        })



