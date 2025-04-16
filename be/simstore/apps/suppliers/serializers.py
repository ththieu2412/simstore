from rest_framework import serializers
from .models import Supplier, ImportReceipt, SIM, ImportReceiptDetail, Employee
import re
from core.constants import DATE_OUTPUT_FORMAT
from datetime import datetime

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

    def validate_name(self, value):
        """Tên không được để trống và có ít nhất 3 ký tự"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Tên nhà cung cấp phải có ít nhất 3 ký tự.")
        return value

    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại hợp lệ (10-15 số)"""
        if value:
            pattern = r"^\+?\d{10,15}$"
            if not re.match(pattern, value):
                raise serializers.ValidationError("Số điện thoại không hợp lệ.")
        return value

    def validate_email(self, value):
        """Kiểm tra định dạng email hợp lệ"""
        if value and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise serializers.ValidationError("Email phải có định dạng hợp lệ (ví dụ: example@domain.com).")
        return value


class SIMSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIM
        fields = ["phone_number", "mobile_network_operator", "category_1", "category_2", "employee", "status"]


class SupplierMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name"]


class SIMCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIM
        fields = ["phone_number", "mobile_network_operator", "category_1", "category_2"]
        extra_kwargs = {
            "phone_number": {"validators": []},  # Tắt validation mặc định
        }

    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại đã tồn tại"""
        existing_sim = SIM.objects.filter(phone_number=value).first()
        if existing_sim:
            raise serializers.ValidationError(f"Số điện thoại '{value}' đã tồn tại trong hệ thống.")
        return value


class SIMRetrieveSerializer(serializers.ModelSerializer):
    mobile_network_operator = serializers.CharField(source="mobile_network_operator.name")
    category_1 = serializers.CharField(source="category_1.name")
    category_2 = serializers.CharField(source="category_2.name")

    class Meta:
        model = SIM
        fields = ["phone_number", "mobile_network_operator", "category_1", "category_2"]


class ImportReceiptDetailCreateSerializer(serializers.ModelSerializer):
    sim = SIMCreateSerializer()  

    class Meta:
        model = ImportReceiptDetail
        fields = ["sim", "import_price"]


class ImportReceiptDetailRetrieveSerializer(serializers.ModelSerializer):
    sim = SIMRetrieveSerializer()  

    class Meta:
        model = ImportReceiptDetail
        fields = ["sim", "import_price"]


class ImportReceiptCreateSerializer(serializers.ModelSerializer):
    sim_list = ImportReceiptDetailCreateSerializer(many=True)  

    class Meta:
        model = ImportReceipt
        fields = ["supplier", "employee", "note", "sim_list"]

class ImportReceiptRetrieveSerializer(serializers.ModelSerializer):
    sim_list = serializers.SerializerMethodField()
    supplier = SupplierMinimalSerializer()
    employee = EmployeeSerializer()
    created_at = serializers.SerializerMethodField()  # Thêm SerializerMethodField

    class Meta:
        model = ImportReceipt
        fields = ["id", "created_at", "note", "supplier", "employee", "sim_list"]

    def get_created_at(self, obj):
        """Format created_at theo định dạng DATE_OUTPUT_FORMAT"""
        if obj.created_at:
            return obj.created_at.strftime(DATE_OUTPUT_FORMAT)
        return None

    def get_sim_list(self, obj):
        """Lấy danh sách SIM từ ImportReceiptDetail"""
        details = ImportReceiptDetail.objects.filter(import_receipt=obj)
        return ImportReceiptDetailRetrieveSerializer(details, many=True).data




