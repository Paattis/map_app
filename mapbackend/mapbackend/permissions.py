from rest_framework import permissions


class IsEditingOwnContent(permissions.BasePermission):
    """
    Only allows owners of an object and admins to edit/delete it
    """

    def has_object_permission(self, request, view, obj):
        # allow read operations
        if request.method in permissions.SAFE_METHODS:
            return True
        print("user", obj.user, "req user", request.user)
        return (obj.user == request.user) or (request.user.is_staff) or (request.user.is_superuser)

