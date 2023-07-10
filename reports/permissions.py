from rest_framework.permissions import BasePermission


class CanViewReportList(BasePermission):
    def has_permission(self, request, view):
        # Allow admins to view all reports, trainers to view their own reports, and clients to view their assigned reports
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer' and view.action == 'list':
            return True
        elif request.user.role == 'client' and view.action == 'list':
            return True
        return False


class CanViewReportDetails(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins to view all reports, trainers to view their own reports, and clients to view their assigned reports
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer' and obj.trainer == request.user:
            return True
        elif request.user.role == 'client' and obj.client == request.user:
            return True
        return False


class CanCreateReport(BasePermission):
    def has_permission(self, request, view):
        # Allow admins and trainers to create reports
        return request.user.role == 'admin' or request.user.role == 'trainer'


class CanUpdateReport(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow trainers, admins, and the assigned client to update reports
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer':
            return True
        elif request.user.role == 'client' and view.action == 'partial_update':
            return True
        return False


class CanDeleteReport(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow trainers to delete reports they made, and admins to delete all reports
        if request.user.role == 'admin':
            return True
        elif request.user.role == 'trainer' and obj.trainer == request.user:
            return True
        return False
