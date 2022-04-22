from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомный класс пагинатора.

    Переопределил количество элементов на странице.
    Переопределил параметр запроса.
    """
    page_size = 2
    page_size_query_param = 'limit'
