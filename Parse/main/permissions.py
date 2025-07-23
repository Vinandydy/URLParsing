from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
    message = 'This bookmark cannot be added'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.time_deleted is None and obj.user == request.user:
            return True
        return False