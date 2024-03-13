from rest_framework import permissions

class IsHospitalUser(permissions.BasePermission):
    """
    Custom permission to only allow hospital users to access a view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_hospital

class IsDoctorUser(permissions.BasePermission):
    """
    Custom permission to only allow doctor users to access a view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor

class IsPatientUser(permissions.BasePermission):
    """
    Custom permission to only allow patient users to access a view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient
