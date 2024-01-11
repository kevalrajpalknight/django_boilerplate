from rest_framework import authentication, permissions


class AdminMixin:
    """
    Mixin for admin-specific views.

    - Requires admin user permissions.
    - Uses session authentication.
    """

    permission_classes = [permissions.IsAdminUser]
