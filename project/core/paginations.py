from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    """
    Custom pagination class for handling pagination of query results.

    Attributes:
        page_size (int): The number of items to be displayed per page. Default is 10.
        page_size_query_param (str): The name of the query parameter used to specify the number of items to be displayed per page. Default is "limit".
        max_page_size (int): The maximum number of items that can be displayed per page. Default is 1000.
    """
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000