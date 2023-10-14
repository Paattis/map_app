from rest_framework import permissions


class IsEditingOwnContent(permissions.BasePermission):
    """
    Only allows owners of an object and admins to edit/delete it
    """

    def has_object_permission(self, request, view, obj):
        # allow read operations
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            (obj.user == request.user)
            or (request.user.is_staff)
            or (request.user.is_superuser)
        )


class IsAdminOrUserItself(permissions.BasePermission):
    """Allow users to access their own data."""

    def has_object_permission(self, request, view, obj):
        return (
            (obj.pk == request.user.id)
            or (request.user.is_staff)
            or (request.user.is_superuser)
        )
