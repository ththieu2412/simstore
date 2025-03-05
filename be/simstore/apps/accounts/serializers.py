from rest_framework import serializers
from .models import Employee, Account, Role
import re
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password


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
        today = timezone.now().date()
        min_birth_date = today - timedelta(days=15*365)  # Trừ 15 năm

        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        if value > min_birth_date:
            raise serializers.ValidationError("You must be at least 15 years old.")

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
        fields = ['id', 'username', 'password', 'role', 'employee', 'status']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def validate_username(self, value):
    #     """Kiểm tra username chỉ chứa chữ cái và số"""
    #     if not value.isalnum():
    #         raise serializers.ValidationError("Username chỉ được chứa chữ cái và số.")
    #     return value

    def validate_password(self, value):
        """Kiểm tra mật khẩu ít nhất 8 ký tự, chứa chữ hoa, chữ thường, số và ký tự đặc biệt"""
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một số.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một chữ hoa.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một chữ thường.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:'\",.<>?/" for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một ký tự đặc biệt.")
        return value

    def create(self, validated_data):
        """Mã hóa mật khẩu trước khi lưu"""
        password = make_password(validated_data['password'])
        print(len(password))  # Kiểm tra độ dài của mật khẩu mã hóa
        validated_data['password'] = password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Cập nhật tài khoản và mã hóa mật khẩu nếu có"""
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
    
    # def to_representation(self, instance):
    #     """Loại bỏ trường mật khẩu khi trả về dữ liệu"""
    #     representation = super().to_representation(instance)
    #     # Loại bỏ trường mật khẩu
    #     representation.pop('password', None)
    #     return representation

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def validate_role_name(self, value):
        """Chuẩn hóa role_name về dạng viết thường và kiểm tra trùng"""
        normalized_name = value.strip().lower()  # Xóa khoảng trắng và chuyển về lowercase

        # Kiểm tra xem có role nào đã tồn tại với tên tương tự không
        if Role.objects.filter(role_name__iexact=normalized_name).exists():
            raise serializers.ValidationError("Role name already exists.")

        return normalized_name

    def create(self, validated_data):
        """Ghi đè create để lưu role_name chuẩn hóa"""
        validated_data['role_name'] = validated_data['role_name'].strip().lower()  # Đảm bảo lưu chuẩn hóa
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        """Kiểm tra dữ liệu đầu vào"""
        if not data.get("username") or not data.get("password"):
            raise serializers.ValidationError("Username và password không được để trống.")
        return data

