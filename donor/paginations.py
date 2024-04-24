from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size=6
    max_page_size=9