from rest_framework.pagination import CursorPagination

class SafeCursorPagination(CursorPagination):
    ordering = ['-created_at', '-id']
    page_size = 5