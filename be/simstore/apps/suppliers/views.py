from django.db import transaction
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from .models import Supplier, ImportReceipt, ImportReceiptDetail, SIM
from .serializers import SupplierSerializer, ImportReceiptCreateSerializer, ImportReceiptRetrieveSerializer
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
    queryset = ImportReceipt.objects.select_related("supplier", "employee").prefetch_related("importreceiptdetail_set")

    def get_serializer_class(self):
        """Chọn serializer phù hợp dựa trên loại yêu cầu"""
        if self.action in ["create", "update"]:
            return ImportReceiptCreateSerializer
        return ImportReceiptRetrieveSerializer

    def create(self, request, *args, **kwargs):
        """Xử lý yêu cầu tạo mới"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            with transaction.atomic():
                supplier = validated_data.get("supplier")
                employee = validated_data.get("employee")

                if not supplier.status:
                    return api_response(
                        status.HTTP_400_BAD_REQUEST,
                        errors={"supplier": "Nhà cung cấp đã ngừng hoạt động, không thể tạo phiếu nhập."}
                    )

                if not employee.status:
                    return api_response(
                        status.HTTP_400_BAD_REQUEST,
                        errors={"employee": "Nhân viên đã nghỉ việc, không thể tạo phiếu nhập."}
                    )
                
                if not employee.account.is_active:
                    return api_response(
                        status.HTTP_400_BAD_REQUEST,
                        errors={"account": "Tài khoản của nhân viên đã bị vô hiệu hóa, không thể tạo phiếu nhập."}
                    )

                sim_data_list = validated_data.pop("sim_list", [])
                import_receipt = ImportReceipt.objects.create(**validated_data)

                self._create_sim_and_details(import_receipt, sim_data_list)

            # Trả về phản hồi
            response_serializer = ImportReceiptRetrieveSerializer(import_receipt)
            return api_response(status.HTTP_201_CREATED, data=response_serializer.data)

        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def _create_sim_and_details(self, import_receipt, sim_data_list):
        """Tạo SIM và ghi vào ImportReceiptDetail"""
        for sim_data in sim_data_list:
            sim_info = sim_data["sim"]
            import_price = sim_data["import_price"]

            sim = SIM.objects.create(**sim_info)

            ImportReceiptDetail.objects.create(
                import_receipt=import_receipt,
                sim=sim,
                import_price=import_price,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Xóa ImportReceipt nếu không có SIM nào liên quan đã được sử dụng trong Order.
        """
        instance = self.get_object()

        related_sims = SIM.objects.filter(importReceiptDetail__import_receipt=instance)

        used_sims = related_sims.filter(order__isnull=False).distinct()

        if used_sims.exists():
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể xóa phiếu nhập vì có SIM đã được sử dụng trong đơn hàng."
            )

        # Nếu không có SIM nào được sử dụng, cho phép xóa
        self.perform_destroy(instance)
        return api_response(status.HTTP_204_NO_CONTENT)