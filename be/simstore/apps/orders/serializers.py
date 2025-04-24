import re
import uuid
from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import Order, Customer, Payment, Discount
from core.constants import DATE_INPUT_FORMATS, DATE_OUTPUT_FORMAT

class CustomerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        format=DATE_OUTPUT_FORMAT,
        read_only=True,
    )

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["created_at"]

    def validate_phone_number(self, phone_number):
        """Kiểm tra tính hợp lệ của số điện thoại."""
        # Định dạng số điện thoại hợp lệ (ví dụ: 10-11 chữ số, bắt đầu bằng 0)
        pattern = r"^0\d{9,10}$"
        if not re.match(pattern, phone_number):
            raise serializers.ValidationError("Số điện thoại không hợp lệ. Số điện thoại phải bắt đầu bằng 0 và có 10-11 chữ số.")
        return phone_number

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        default=timezone.now,
        format=DATE_OUTPUT_FORMAT,
        input_formats=DATE_INPUT_FORMATS,
        read_only=True,
    )
    address = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField() 
    sim_export_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["address"]

    def get_address(self, obj):
        """Trả về địa chỉ đầy đủ của khách hàng."""
        if obj.ward:
            return f"{obj.detailed_address}, {obj.ward.name}, {obj.ward.district.name}, {obj.ward.district.province.name}"
        return None

    def to_representation(self, instance):
        """Tùy chỉnh dữ liệu trả về."""
        data = super().to_representation(instance)
        data["status_order"] = instance.get_status_order_display()
        data["sim"] = instance.sim.phone_number if instance.sim else None
        data["customer"] = instance.customer.full_name if instance.customer else None

        # Loại bỏ các trường không cần thiết
        # data.pop("ward", None)
        # data.pop("detailed_address", None)
        return data
    
    def get_discount_percentage(self, obj):
        """Lấy giá trị percentage từ mã giảm giá."""
        if obj.discount:
            return obj.discount.percentage
        return None
    
    def get_sim_export_price(self, obj):
        """Lấy giá bán (export_price) của SIM."""
        if obj.sim:
            return obj.sim.export_price  # Trả về giá bán của SIM
        return None


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def update(self, instance, validated_data):
        """Cập nhật thời gian chỉnh sửa."""
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)


class DiscountSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        format=DATE_OUTPUT_FORMAT,
    )
    end_date = serializers.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        format=DATE_OUTPUT_FORMAT,
    )

    class Meta:
        model = Discount
        fields = "__all__"
        read_only_fields = ["status", "discount_code"]

    def validate(self, data):
        """Kiểm tra tính hợp lệ của dữ liệu."""
        self._validate_percentage(data.get("percentage"))
        self._validate_date_range(data.get("start_date"), data.get("end_date"))
        return data

    def _validate_percentage(self, percentage):
        """Kiểm tra phần trăm giảm giá hợp lệ."""
        if percentage is not None and (percentage < 0 or percentage >= 100):
            raise serializers.ValidationError(
                {"percentage": "Phần trăm giảm giá phải lớn hơn 0 và nhỏ hơn 100."}
            )

    def _validate_date_range(self, start_date, end_date):
        """Kiểm tra start_date < end_date."""
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                {"start_date": "Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc."}
            )

    def validate_employee(self, employee):
        """Kiểm tra trạng thái của nhân viên và tài khoản."""
        if not employee.account.is_active:  # Tài khoản bị vô hiệu hóa
            raise serializers.ValidationError("Tài khoản của nhân viên đã bị vô hiệu hóa, không thể thực hiện thao tác.")
        return employee

    def create(self, validated_data):
        """Tự động tạo discount_code duy nhất."""
        validated_data["discount_code"] = f"MGG{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)

    def to_representation(self, instance):
        """Tùy chỉnh dữ liệu trả về."""
        data = super().to_representation(instance)
        data["start_date"] = self._format_datetime(instance.start_date)
        data["end_date"] = self._format_datetime(instance.end_date)
        return data

    def _format_datetime(self, value):
        """Định dạng lại datetime."""
        if value:
            if timezone.is_naive(value):
                value = timezone.make_aware(value)
            return timezone.localtime(value).strftime(DATE_OUTPUT_FORMAT)
        return None
