from rest_framework import serializers
from .models import Supplier
import re

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def validate_name(self, value):
        """Tên không được để trống và có ít nhất 3 ký tự"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Tên nhà cung cấp phải có ít nhất 3 ký tự.")
        return value

    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại hợp lệ (10-15 số)"""
        if value:
            pattern = r'^\+?\d{10,15}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("Số điện thoại không hợp lệ.")
        return value

    def validate_email(self, value):
        """Chỉ chấp nhận email có đuôi @gmail.com hoặc để trống"""
        if value and not re.match(r'^[\w\.-]+@gmail\.com$', value):
            raise serializers.ValidationError("Email phải có định dạng xxx@gmail.com.")
        return value
