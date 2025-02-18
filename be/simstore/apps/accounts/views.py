from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import EmployeeSerializer, AccountSerializer, RoleSerializer
from .models import Employee, Account, Role
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

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

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
