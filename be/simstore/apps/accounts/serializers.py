from rest_framework import serializers
from .models import Employee, Account
import re
from django.utils import timezone


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_phone_number(self, value):
        # Kiểm tra số điện thoại hợp lệ (chỉ chứa số và độ dài từ 10-15 ký tự)
        if not re.match(r'^\d{10,15}$', value):
            raise serializers.ValidationError("Phone number must be numeric and between 10 and 15 digits.")
        return value

    def validate_citizen_id(self, value):
        # Kiểm tra xem citizen_id có đúng 12 ký tự không
        if len(value) != 12:
            raise serializers.ValidationError("Citizen ID must be 12 characters long.")
        return value

    def validate_date_of_birth(self, value):
        # Kiểm tra ngày sinh không phải trong tương lai
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_gender(self, value):
        # Kiểm tra giá trị của gender (0 hoặc 1)
        if value not in [True, False]:
            raise serializers.ValidationError("Gender must be either True or False.")
        return value

    def validate_avatar(self, value):
        # Kiểm tra nếu có avatar thì phải là ảnh hợp lệ
        if value:
            if not value.name.endswith(('jpg', 'jpeg', 'png')):
                raise serializers.ValidationError("Avatar must be a jpg, jpeg, or png image.")
            if value.size > 5 * 1024 * 1024:  # 5MB limit
                raise serializers.ValidationError("Avatar file size must be less than 5MB.")
        return value

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
