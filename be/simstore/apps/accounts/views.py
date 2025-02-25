from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import EmployeeSerializer, AccountSerializer, RoleSerializer, LoginSerializer
from .models import Employee, Account, Role
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from django.db.models import ProtectedError
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
    
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

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
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """API Login - Xác thực bằng Token"""
        print("Kiểm tra data nhập vào")
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                account = Account.objects.get(username=username)
                if not account.is_active:
                    return Response(
                        {"error": "Account is inactive. Please contact the administrator."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                if check_password(password, account.password):  # Kiểm tra mật khẩu
                    token, _ = Token.objects.get_or_create(user=account)
                    return Response({
                        "statuscode": status.HTTP_200_OK,
                        "data": {
                            "token": token.key,
                            "username": account.username,
                            "role": account.role.role_name
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

