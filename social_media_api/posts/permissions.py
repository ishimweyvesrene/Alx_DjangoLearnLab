# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Safe methods allowed for everyone. Write methods only allowed to owners.
    """
    def has_object_permission(self, request, view, obj):
        # read-only allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # obj must have an `author` attribute
        return getattr(obj, 'author', None) == request.user
