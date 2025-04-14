from rest_framework import viewsets, status
from .models import Supplier, ImportReceipt
from .serializers import SupplierSerializer, ImportReceiptSerializer
from utils import api_response


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        """
        Lọc danh sách nhà cung cấp theo các thuộc tính.
        """
        queryset = super().get_queryset()
        query_params = self.request.query_params

        filters = {
            "id": query_params.get("id"),
            "name__icontains": query_params.get("name"),
            "phone_number__icontains": query_params.get("phone_number"),
            "email__icontains": query_params.get("email"),
            "address__icontains": query_params.get("address"),
        }

        # Lọc theo trạng thái (status)
        status = query_params.get("status")
        if status is not None:
            filters["status"] = status.lower() in ["true", "1"]

        # Áp dụng bộ lọc
        return queryset.filter(**{k: v for k, v in filters.items() if v is not None})

    def create(self, request, *args, **kwargs):
        """Tạo mới nhà cung cấp"""
        return self._handle_request(request, self.perform_create, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin nhà cung cấp"""
        return self._handle_request(request, self.perform_update, status.HTTP_200_OK, partial=kwargs.pop("partial", False))

    def destroy(self, request, *args, **kwargs):
        """Xóa nhà cung cấp"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(status.HTTP_204_NO_CONTENT)

    def _handle_request(self, request, action, success_status, partial=False):
        """
        Xử lý các yêu cầu CRUD chung (create, update).
        """
        instance = self.get_object() if action == self.perform_update else None
        serializer = self.get_serializer(instance, data=request.data, partial=partial) if instance else self.get_serializer(data=request.data)

        if serializer.is_valid():
            action(serializer)
            return api_response(success_status, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class ImportReceiptViewSet(viewsets.ModelViewSet):
    queryset = ImportReceipt.objects.all()
    serializer_class = ImportReceiptSerializer

    def create(self, request, *args, **kwargs):
        """Tạo mới phiếu nhập"""
        return self._handle_request(request, self.perform_create, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Cập nhật phiếu nhập"""
        return self._handle_request(request, self.perform_update, status.HTTP_200_OK, partial=kwargs.pop("partial", False))

    def _handle_request(self, request, action, success_status, partial=False):
        """
        Xử lý các yêu cầu CRUD chung (create, update).
        """
        instance = self.get_object() if action == self.perform_update else None
        serializer = self.get_serializer(instance, data=request.data, partial=partial) if instance else self.get_serializer(data=request.data)

        if serializer.is_valid():
            action(serializer)
            return api_response(success_status, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

