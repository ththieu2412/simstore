import re
from django.utils import timezone
from rest_framework import serializers
from .models import Order, Customer, Payment, Discount
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
import uuid

class CustomerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S",   # 2025-03-04 08:30:00
            "%Y-%m-%dT%H:%M:%SZ",  # 2025-03-04T08:30:00Z (ISO 8601)
            "%Y-%m-%dT%H:%M:%S%z", # 2025-03-04T08:30:00+07:00
        ],
        format="%H:%M:%S %Y-%m-%d"
    )
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["created_at"]

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        default=now,
        format="%H:%M:%S %Y-%m-%d",
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
        ],
    )

    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["address"]

    def get_address(self, obj):
        """
        Trả về địa chỉ đầy đủ của khách hàng.
        """
        if obj.ward:
            return f"{obj.detailed_address}, {obj.ward.name}, {obj.ward.district.name}, {obj.ward.district.province.name}"
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status_order"] = instance.get_status_order_display()
        data["sim"] = instance.sim.phone_number if instance.sim else None
        data["customer"] = instance.customer.full_name if instance.customer else None

        data.pop("ward", None)
        data.pop("detailed_address", None)
        
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)

class DiscountSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S",   # 2025-03-04 08:30:00
            "%Y-%m-%dT%H:%M:%SZ",  # 2025-03-04T08:30:00Z (ISO 8601)
            "%Y-%m-%dT%H:%M:%S%z", # 2025-03-04T08:30:00+07:00
        ],
        format="%H:%M:%S %Y-%m-%d"
    )

    end_date = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
        ],
        format="%H:%M:%S %Y-%m-%d"
    )
    class Meta:
        model = Discount
        fields = '__all__'
        read_only_fields = ['status', 'discount_code']

    def validate(self, data):
        """
        Kiểm tra start_date < end_date.
        """
        percentage = data.get('percentage')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Kiểm tra phần trăm giảm giá hợp lệ
        if percentage is not None and (percentage < 0 or percentage >= 100):
            raise serializers.ValidationError({"percentage": "Phần trăm giảm giá phải lớn hơn 0 và nhỏ hơn 100."})

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError({"start_date": "Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc."})

        return data

    def validate_employee(self, employee):
        """
        Kiểm tra trạng thái của nhân viên và tài khoản.
        """
        if employee.status == 0:  # 0: Đã nghỉ việc
            raise serializers.ValidationError("Nhân viên đã nghỉ việc, không thể thực hiện thao tác.")
        if not employee.account.is_active:  # Tài khoản bị vô hiệu hóa
            raise serializers.ValidationError("Tài khoản của nhân viên đã bị vô hiệu hóa, không thể thực hiện thao tác.")
        return employee
    
    def create(self, validated_data):
        """
        Ghi đè phương thức create để tự động tạo discount_code duy nhất.
        """
        validated_data["discount_code"] = f"MGG{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Format lại start_date và end_date trước khi trả về.
        """
        data = super().to_representation(instance)

        def format_datetime(value):
            if value:
                # Nếu `value` không có thông tin về múi giờ, chuyển nó sang aware datetime
                if timezone.is_naive(value):
                    value = timezone.make_aware(value)
                return timezone.localtime(value).strftime("%Y-%m-%d %H:%M:%S")
            return None

        data['start_date'] = format_datetime(instance.start_date)
        data['end_date'] = format_datetime(instance.end_date)

        return data
