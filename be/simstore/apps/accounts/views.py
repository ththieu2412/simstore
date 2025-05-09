# Thư viện Django
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError, Func, Value, Q, BooleanField, Case, When
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404

# Thư viện Django REST Framework
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

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
import os
from django.conf import settings

from urllib.parse import urljoin

# Permissions
from simstore.permissions import IsAdminPermission

from utils import api_response

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet để custom response format
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return api_response(status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể xóa vì có dữ liệu liên quan.",
            )

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return api_response(status.HTTP_200_OK, data=serializer.data)


class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        """
        Cập nhật thông tin nhân viên.
        Nếu status của nhân viên bị vô hiệu hóa, cũng vô hiệu hóa tài khoản liên quan.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            self._deactivate_account_if_needed(instance, serializer.validated_data)
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def _deactivate_account_if_needed(self, employee, validated_data):
        """
        Vô hiệu hóa tài khoản nếu status của nhân viên bị vô hiệu hóa.
        """
        if "status" in validated_data and not validated_data["status"]:
            try:
                account = employee.account
                account.status = False
                account.save()
            except AttributeError:
                pass  

    def get_queryset(self):
        """
        Lọc danh sách nhân viên.
        """
        queryset = super().get_queryset()
        params = self.request.query_params

        # Lọc theo các tham số
        full_name = params.get("full_name")
        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)

        email = params.get("email")
        if email:
            queryset = queryset.filter(email__icontains=email)

        phone_number = params.get("phone_number")
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)

        status = params.get("status")
        if status is not None:
            queryset = queryset.filter(status=status.lower() in ["true", "1"])

        # Lọc nhân viên đã có tài khoản hay chưa
        has_account = params.get("has_account")
        if has_account is not None:
            has_account = has_account.lower() in ["true", "1"]
            queryset = queryset.annotate(
                has_account=Case(
                    When(account__isnull=False, then=True),
                    default=False,
                    output_field=BooleanField(),
                )
            ).filter(has_account=has_account)

        # Lọc theo trạng thái tài khoản
        account_status = params.get("account_status")
        if account_status is not None:
            account_status = account_status.lower() in ["true", "1"]
            queryset = queryset.filter(account__is_active=account_status)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Lấy danh sách nhân viên và sắp xếp trong Python.
        """
        queryset = self.filter_queryset(self.get_queryset())
        employees = list(queryset)
        employees.sort(key=lambda emp: (
            emp.full_name.split()[-1],  # Tên (phần cuối cùng)
            emp.full_name.split()[1:-1],  # Tên đệm (phần giữa)
            emp.full_name.split()[0]  # Họ (phần đầu tiên)
        ))
        page = self.paginate_queryset(employees)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class AccountViewSet(BaseViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        """
        Lọc danh sách tài khoản theo các tham số từ request.
        """
        queryset = super().get_queryset()
        params = self.request.query_params

        username = params.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)

        email = params.get("email")
        if email:
            queryset = queryset.filter(employee__email__icontains=email)

        is_active = params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ["true", "1"])

        role = params.get("role")
        if role:
            queryset = queryset.filter(role__role_name__icontains=role)

        return queryset

    def handle_exception(self, exc):
        """
        Xử lý lỗi permission để trả về đúng format yêu cầu
        """
        if isinstance(exc, IsAdminPermission):
            return api_response(status.HTTP_403_FORBIDDEN, errors="Bạn không có quyền truy cập API này!")
        return super().handle_exception(exc)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        """
        API Login - Xác thực bằng JWT
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return self._authenticate_user(serializer.validated_data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def _authenticate_user(self, validated_data):
        """
        Xác thực người dùng và trả về JWT token.
        """
        username = validated_data["username"]
        password = validated_data["password"]

        try:
            account = Account.objects.get(username=username)

            if check_password(password, account.password):
                if not account.is_active:
                    return api_response(
                        status.HTTP_403_FORBIDDEN, errors="Tài khoản đã bị vô hiệu hóa!"
                    )
                return self._generate_jwt_response(account)
                
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Sai mật khẩu!")
        except Account.DoesNotExist:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Tài khoản không tồn tại!")

    def _generate_jwt_response(self, account):
        """
        Tạo JWT token cho người dùng và trả về link đầy đủ cho ảnh đại diện.
        """
        refresh = RefreshToken.for_user(account)
        request = self.request  

        default_avatar_path = f"{settings.MEDIA_URL}image/avatar_default.png"
        default_avatar_url = request.build_absolute_uri(default_avatar_path) if request else default_avatar_path

        # Nếu nhân viên có ảnh đại diện, trả về link đầy đủ
        avatar_url = (
            request.build_absolute_uri(account.employee.avatar.url)
            if account.employee.avatar and request
            else default_avatar_url
        )

        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "username": account.username,
            "role": account.role.role_name,
            "employee_id": account.employee.id,
            "avatar": avatar_url,  # Trả về link đầy đủ
        }
        return api_response(status.HTTP_200_OK, data=data)


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return api_response(status.HTTP_400_BAD_REQUEST, errors="Refresh token is required")

            token = RefreshToken(refresh_token)
            token.blacklist()  
            return api_response(status.HTTP_200_OK, data="Đăng xuất thành công")
        except Exception as e:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Token không hợp lệ hoặc đã hết hạn")
        
User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Gửi email đặt lại mật khẩu.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email(request)
            return api_response(status.HTTP_200_OK, data="Email đặt lại mật khẩu đã được gửi.")
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        """
        Xác nhận đặt lại mật khẩu.
        """
        user = self._get_user_from_uid(uidb64)
        if not user:
            return api_response(
                status.HTTP_400_BAD_REQUEST, errors="Không thể giải mã UID hoặc tìm thấy người dùng."
            )

        if not default_token_generator.check_token(user, token):
            return api_response(
                status.HTTP_400_BAD_REQUEST, errors="Token không hợp lệ hoặc đã hết hạn."
            )

        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Kiểm tra nếu mật khẩu mới hoặc xác nhận mật khẩu không được cung cấp
        if not new_password or not confirm_password:
            return api_response(
                status.HTTP_400_BAD_REQUEST, errors="Mật khẩu mới và xác nhận mật khẩu là bắt buộc."
            )

        # Kiểm tra nếu mật khẩu mới và xác nhận mật khẩu không khớp
        if new_password != confirm_password:
            return api_response(
                status.HTTP_400_BAD_REQUEST, errors="Mật khẩu mới và xác nhận mật khẩu không khớp."
            )

        # Đặt mật khẩu mới
        user.set_password(new_password)
        user.save()
        return api_response(status.HTTP_200_OK, data="Đặt lại mật khẩu thành công.")

    def _get_user_from_uid(self, uidb64):
        """
        Lấy người dùng từ UID được mã hóa.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return get_object_or_404(get_user_model(), pk=uid)
        except Exception:
            return None

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        Làm mới token bằng refresh_token.
        """
        try:
            response = super().post(request, *args, **kwargs)
            return api_response(
                status.HTTP_200_OK,
                data={
                    "access_token": response.data["access"]  
                },
            )
        except Exception as e:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Token không hợp lệ hoặc đã hết hạn.",
            )
