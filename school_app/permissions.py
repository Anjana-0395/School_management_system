from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'staff'

class IsLibrarianUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'

class IsAdminOrStaff(BasePermission):
    """
    Custom permission to allow only admin or staff to perform write operations.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ['admin', 'staff'])


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin to write, others can read.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
