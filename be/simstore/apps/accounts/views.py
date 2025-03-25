# Thư viện Django
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "statuscode": status.HTTP_201_CREATED,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)

            # Nếu status cập nhật thành False, cập nhật status trong Account
            if "status" in serializer.validated_data and serializer.validated_data["status"] is False:
                try:
                    account = instance.account  # Giả sử có quan hệ OneToOne hoặc ForeignKey
                    account.status = False
                    account.save()
                except AttributeError:
                    pass  # Nếu không có tài khoản, bỏ qua lỗi

            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Không thể xóa nhân viên vì có dữ liệu liên quan."
            }, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({
                "statuscode": status.HTTP_201_CREATED,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_201_CREATED)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Cập nhật Role"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response({
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Không thể xóa role vì có dữ liệu liên quan."
            }, status=status.HTTP_400_BAD_REQUEST)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [IsAdminPermission]
    
    def handle_exception(self, exc):
        """
        Xử lý lỗi permission để trả về đúng format yêu cầu
        """
        if isinstance(exc, IsAdminPermission):
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Bạn không có quyền truy cập API này!"
            }, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        """Tạo tài khoản mới"""
        # print("Kiểm tra data nhập vào")
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "statuscode": status.HTTP_201_CREATED,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_201_CREATED)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Cập nhật tài khoản"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Xóa tài khoản"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "statuscode": status.HTTP_204_NO_CONTENT,
            "data": None,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_204_NO_CONTENT)
    
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
                    return Response({
                        "statuscode": status.HTTP_403_FORBIDDEN,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Tài khoản bị vô hiệu hóa!"
                    }, status=status.HTTP_403_FORBIDDEN)

                if check_password(password, account.password):  # Kiểm tra mật khẩu
                    # Tạo JWT Token
                    refresh = RefreshToken.for_user(account)
                    # update_last_login(None, account)  # Cập nhật thời gian đăng nhập gần nhất

                    return Response({
                        "statuscode": status.HTTP_200_OK,
                        "data": {
                            "access_token": str(refresh.access_token),
                            "refresh_token": str(refresh),
                            "username": account.username,
                            "role": account.role.role_name,
                            "employee_id": account.employee.id
                        },
                        "status": "success",
                        "errorMessage": None
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Sai mật khẩu!"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Account.DoesNotExist:
                return Response({
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Tài khoản không tồn tại!"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Chặn refresh token này (Chỉ hoạt động nếu bật Blacklist)

            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)  
        
User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email(request)
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": None,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)

        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": "Dữ liệu không hợp lệ.",
            "errors": serializer.errors  # Thêm chi tiết lỗi để debug
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                if not new_password:
                    return Response({
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Mật khẩu mới là bắt buộc."
                    }, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({
                    "statuscode": status.HTTP_200_OK,
                    "data": None,
                    "status": "success",
                    "errorMessage": None
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Token không hợp lệ hoặc đã hết hạn."
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Đã xảy ra lỗi.",
                "errors": str(e)  # Hiển thị lỗi chi tiết nếu cần debug
            }, status=status.HTTP_400_BAD_REQUEST)
