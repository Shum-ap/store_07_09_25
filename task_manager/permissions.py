from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает чтение всем, но изменение/удаление только владельцу.
    """
    def has_object_permission(self, request, view, obj):
        # (GET, HEAD, OPTIONS) всем
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # (PUT, PATCH, DELETE) только владельцу
        return obj.owner == request.user