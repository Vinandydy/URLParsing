from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    message = 'This bookmark cannot be added'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.time_deleted is None and obj.user == request.user


class AdminOwnerPermission(permissions.BasePermission):
    def custom_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user