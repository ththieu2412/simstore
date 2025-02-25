from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Supplier, ImportReceipt
from .serializers import SupplierSerializer, ImportReceiptSerializer
from django.utils.timezone import now

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def create(self, request, *args, **kwargs):
        """Tạo mới nhà cung cấp với response format chuẩn"""
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
        """Cập nhật toàn bộ thông tin nhà cung cấp"""
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
        """Xóa nhà cung cấp"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": None,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_200_OK)

class ImportReceiptViewSet(viewsets.ModelViewSet):
    queryset = ImportReceipt.objects.all()
    serializer_class = ImportReceiptSerializer

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
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)