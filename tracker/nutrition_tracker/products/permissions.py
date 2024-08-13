from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Любой юзер может смотреть чужие приемы пищи, лучше бы, если только админ мог
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # if request.method == 'POST' and request.user.is_staff:
        #     return True
        # elif request.method in permissions.SAFE_METHODS:
        #     return True
        # return False
    
        if request.method == 'POST' and request.user.is_staff or \
            request.method in permissions.SAFE_METHODS:
            return True
        return False