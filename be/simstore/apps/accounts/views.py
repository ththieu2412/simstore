# Thư viện Django
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404

# Thư viện Django REST Framework
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Models
from .models import Employee, Account, Role

# Serializers
from .serializers import (
    EmployeeSerializer, 
    AccountSerializer, 
    RoleSerializer, 
    LoginSerializer, 
    PasswordResetRequestSerializer
)

# Permissions
from simstore.permissions import IsAdminPermission

from utils import api_response

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        else:
            return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            # Nếu employee.status cập nhật thành False, cập nhật status trong Account
            if "status" in serializer.validated_data and not serializer.validated_data["status"]:
                try:
                    account = instance.account 
                    account.status = False
                    account.save()
                except AttributeError:
                    pass  # Nếu không có tài khoản, bỏ qua lỗi

            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return api_response(status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Không thể xóa nhân viên vì có dữ liệu liên quan.")

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        """Tạo Role mới"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """Cập nhật Role"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return api_response(status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể xóa role vì có dữ liệu liên quan.",
            )

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [IsAdminPermission]
    
    def handle_exception(self, exc):
        """
        Xử lý lỗi permission để trả về đúng format yêu cầu
        """
        if isinstance(exc, IsAdminPermission):
            return api_response(status.HTTP_403_FORBIDDEN, errors="Bạn không có quyền truy cập API này!")
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """API Login - Xác thực bằng JWT"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                account = Account.objects.get(username=username)
                if not account.is_active:
                    return api_response(status.HTTP_403_FORBIDDEN, errors="Tài khoản đã bị vô hiệu hóa!")
                
                if check_password(password, account.password):  # Kiểm tra mật khẩu
                    # Tạo JWT Token
                    refresh = RefreshToken.for_user(account)
                    data = {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "username": account.username,
                        "role": account.role.role_name,
                        "employee_id": account.employee.id
                    }
                    return api_response(status.HTTP_200_OK, data=data)
                return api_response(status.HTTP_400_BAD_REQUEST, errors="Sai mật khẩu!")
            except Account.DoesNotExist:
                return api_response(status.HTTP_400_BAD_REQUEST, errors="Tài khoản không tồn tại!")
            except Exception as e:
                return api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, errors=f"Lỗi server: {str(e)}")
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return api_response(status.HTTP_400_BAD_REQUEST, errors="Refresh token is required")

            token = RefreshToken(refresh_token)
            token.blacklist()  # Chặn refresh token này (Chỉ hoạt động nếu bật Blacklist)
            return api_response(status.HTTP_200_OK, data="Đăng xuất thành công")
        except Exception as e:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Invalid token")
        
User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email(request)
            return api_response(status.HTTP_200_OK)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                if not new_password:
                    return api_response(
                        status.HTTP_400_BAD_REQUEST,
                        errors="Mật khẩu mới là bắt buộc.",
                    )

                user.set_password(new_password)
                user.save()
                return api_response(status.HTTP_200_OK)
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                message="Token không hợp lệ hoặc đã hết hạn.",
            )

        except Exception as e:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                message="Đã xảy ra lỗi.",
                errors=str(e),
            )
