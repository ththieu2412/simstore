import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import serializers

from .models import Account, Employee, Role

from django.conf import settings

from validators import (
    validate_phone_number,
    validate_citizen_id,
    validate_date_of_birth,
    validate_avatar,
    validate_password,
)


class EmployeeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_phone_number(self, value):
        return validate_phone_number(value)

    def validate_citizen_id(self, value):
        return validate_citizen_id(value)

    def validate_date_of_birth(self, value):
        return validate_date_of_birth(value)

    def validate_avatar(self, value):
        return validate_avatar(value)

    def get_avatar(self, obj):
        """Trả về URL của avatar hoặc ảnh mặc định"""
        request = self.context.get("request")  
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        
        default_avatar_url = f"{settings.MEDIA_URL}image/avatar_default.png"
        return request.build_absolute_uri(default_avatar_url) if request else default_avatar_url


class AccountSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = Account
        fields = ["id", "username", "password", "role", "employee", "employee_name", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        return validate_password(value)

    def create(self, validated_data):
        """Mã hóa mật khẩu trước khi lưu"""
        password = make_password(validated_data["password"])
        validated_data["password"] = password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Cập nhật tài khoản và mã hóa mật khẩu nếu có"""
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

    def validate_role_name(self, value):
        """Chuẩn hóa role_name về dạng viết thường và kiểm tra trùng"""
        normalized_name = value.strip().lower()

        if Role.objects.filter(role_name__iexact=normalized_name).exists():
            raise serializers.ValidationError("Role name already exists.")

        return normalized_name

    def create(self, validated_data):
        """Ghi đè create để lưu role_name chuẩn hóa"""
        validated_data["role_name"] = validated_data["role_name"].strip().lower()
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Account
        fields = ["employee"]

    def validate(self, data):
        """Kiểm tra dữ liệu đầu vào"""
        if not data.get("username") or not data.get("password"):
            raise serializers.ValidationError("Username và password không được để trống.")
        return data


User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Kiểm tra email tồn tại và tài khoản không bị vô hiệu hóa"""
        try:
            employee = Employee.objects.get(email=value) 
            if not employee.status:
                raise serializers.ValidationError("Tài khoản này đã bị vô hiệu hóa.")
            user = Account.objects.get(employee=employee) 
        except (Employee.DoesNotExist, Account.DoesNotExist):
            raise serializers.ValidationError("Email không tồn tại trong hệ thống.")
        return value

    def send_reset_email(self, request):
        """Gửi email đặt lại mật khẩu"""
        email = self.validated_data["email"]
        employee = Employee.objects.get(email=email)
        user = Account.objects.get(employee=employee)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse("password-reset-confirm", kwargs={"uidb64": uid, "token": token})
        )

        # Gửi email
        send_mail(
            "Password Reset Request",
            f"Click the link below to reset your password:\n{reset_url}",
            "ththieu2412@gmail.com",
            [email],
            fail_silently=False,
        )