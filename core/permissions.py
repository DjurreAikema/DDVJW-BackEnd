from rest_framework.permissions import BasePermission


class CanViewUserList(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins to see all users, trainers to see themselves and users they are assigned to, and clients only themselves
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer' and (obj == request.user or obj.trainer == request.user):
            return True
        elif request.user.role == 'client' and obj == request.user:
            return True
        return False


class CanViewUserDetails(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins ti see all users, trainers to see themselves and users they are assigned to, and clients only themselves
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer' and (obj == request.user or obj.trainer == request.user):
            return True
        elif request.user.role == 'client' and obj == request.user:
            return True
        return False


class CanCreateUser(BasePermission):
    def has_permission(self, request, view):
        # Allow only admins to create users
        return request.user.role == 'admin'


class CanUpdateUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins to update all users, trainers only themselves, and clients only themselves
        if request.user.role == 'admin':
            return True
        elif (request.user.role == 'trainer' or request.user.role == 'client') and obj == request.user:
            return True
        return False


class CanDeleteUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins to delete all users, trainers only themselves, and clients only themselves
        if request.user.role == 'admin':
            return True
        elif (request.user.role == 'trainer' or request.user.role == 'client') and obj == request.user:
            return True
        return False
