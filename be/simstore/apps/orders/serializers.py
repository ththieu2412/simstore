from django.utils import timezone
from rest_framework import serializers
from .models import Order, Customer, Payment, Discount
from django.utils.timezone import now

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
            raise serializers.ValidationError({"start_date": "Ngày bắt đầu phải nhỏ hơn ngày kết thúc."})

        return data

    def create(self, validated_data):
        """
        Xử lý logic status trước khi lưu.
        """
        start_date = validated_data.get('start_date')

        # Nếu start_date > hiện tại thì status = False (chưa có hiệu lực)
        validated_data['status'] = start_date > now()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Cập nhật status khi sửa.
        """
        start_date = validated_data.get('start_date', instance.start_date)

        # Cập nhật status theo start_date
        validated_data['status'] = start_date > now()

        return super().update(instance, validated_data)
