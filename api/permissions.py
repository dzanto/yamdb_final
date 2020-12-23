from rest_framework import permissions
from rest_framework.permissions import BasePermission


class ReviewCreatePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'POST'):
            return True
        if request.method in ('DELETE', 'PATCH'):
            return request.user == obj.author


class AdminResourcePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in (
                'DELETE', 'POST',
                'PATCH') and request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return True


class StaffResourcePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in (
                'DELETE', 'PATCH') and request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_moderator
        return True


class IsOwnerOrReadOnly(BasePermission):
    """ 
    Custom permission to only allow owners of an object to edit it. 
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, 
        # so we'll always allow GET, HEAD or OPTIONS requests. 
        if request.method in permissions.SAFE_METHODS:
            return True

            # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user


class SiteAdminPermission(permissions.BasePermission):
    def has_permission(self, request, obj):

        if request.method == 'GET':
            return request.user.is_authenticated or not request.user.is_authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.is_authenticated

        return request.user.is_superuser or request.user.is_admin or request.user.is_moderator
