from rest_framework import permissions


class IsOwnerOrAdminOnly(permissions.IsAuthenticated):
    """
    Custom permission to only allow owners of an object and administrators to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow administrators to perform any request
        if request.user.is_staff:
            return True

        # Allow owners to read or edit their own details
        return obj == request.user
