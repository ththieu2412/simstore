from django.utils import timezone
from rest_framework import serializers
from .models import Order, Customer, Payment, Discount
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

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
        format="%Y-%m-%d %H:%M:%S"
    )
    end_date = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
        ],
        format="%Y-%m-%d %H:%M:%S"
    )
    class Meta:
        model = Discount
        fields = '__all__'
        read_only_fields = ['status']  # Không cho phép nhập trực tiếp status

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

    # def create(self, validated_data):
    #     """
    #     Xử lý logic status trước khi lưu.
    #     """
    #     start_date = validated_data.get('start_date')

    #     # Nếu start_date > hiện tại thì status = False (chưa có hiệu lực)
    #     validated_data['status'] = start_date < now()

    #     return super().create(validated_data)


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
