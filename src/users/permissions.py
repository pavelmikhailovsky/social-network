from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    """
    Allow access only to not authentication users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)
