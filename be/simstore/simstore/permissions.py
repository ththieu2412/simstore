from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

class IsAdminPermission(BasePermission):
    """
    Chỉ cho phép Admin truy cập API
    """
    def has_permission(self, request, view):
        # Kiểm tra xem user có đăng nhập không
        if not request.user.is_authenticated:
            return False

        # Kiểm tra role có phải Admin không
        user_role = request.user.role.role_name if request.user.role else ""
        return user_role.lower() == "admin"

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
