from rest_framework.permissions import BasePermission


class CanViewSchoolList(BasePermission):
    def has_permission(self, request, view):
        # Allow admins and trainers to view all schools
        return request.user.role == 'admin' or request.user.role == 'trainer'


class CanViewSchoolDetails(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins and trainers to view a school
        return request.user.role == 'admin' or request.user.role == 'trainer'


class CanCreateSchool(BasePermission):
    def has_permission(self, request, view):
        # Allow admins to create schools
        return request.user.role == 'admin'


class CanUpdateSchool(BasePermission):
    def has_permission(self, request, view):
        # Allow admins to update schools
        return request.user.role == 'admin'


class CanDeleteSchool(BasePermission):
    def has_permission(self, request, view):
        # Allow admins to delete schools
        return request.user.role == 'admin'
