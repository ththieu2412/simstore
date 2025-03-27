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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại hợp lệ (chỉ chứa số và độ dài từ 10-15 ký tự)"""
        if not re.match(r"^\d{10,15}$", value):
            raise serializers.ValidationError(
                "Số điện thoại không hợp lệ (phải từ 10 đến 15 chữ số)."
            )
        return value

    def validate_citizen_id(self, value):
        """Kiểm tra xem citizen_id có đúng 12 ký tự không"""
        if len(value) != 12:
            raise serializers.ValidationError("CCCD bắt buộc 12 ký tự số.")
        return value

    def validate_date_of_birth(self, value):
        """Kiểm tra ngày sinh hợp lệ (không tương lai, ít nhất 15 tuổi)"""
        today = timezone.now().date()
        min_birth_date = today - timedelta(days=15 * 365)  # Trừ 15 năm

        if value > today:
            raise serializers.ValidationError("Ngày sinh không hợp lệ.")
        if value > min_birth_date:
            raise serializers.ValidationError("Nhân viên phải lớn hơn 15 tuổi.")

        return value

    def validate_avatar(self, value):
        """Kiểm tra avatar là ảnh hợp lệ và dưới 5MB"""
        if value:
            if not value.name.endswith(("jpg", "jpeg", "png")):
                raise serializers.ValidationError(
                    "Avatar must be a jpg, jpeg, or png image."
                )
            if value.size > 5 * 1024 * 1024:  # 5MB limit
                raise serializers.ValidationError(
                    "Avatar file size must be less than 5MB."
                )
        return value


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "password", "role", "employee", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        """Kiểm tra mật khẩu ít nhất 8 ký tự, chứa chữ hoa, thường, số và ký tự đặc biệt"""
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một số.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một chữ hoa.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một chữ thường.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:'\",.<>?/" for char in value):
            raise serializers.ValidationError(
                "Mật khẩu phải chứa ít nhất một ký tự đặc biệt."
            )
        return value

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
        normalized_name = value.strip().lower()  # Xóa khoảng trắng và chuyển về lowercase

        # Kiểm tra xem có role nào đã tồn tại với tên tương tự không
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

        # Tạo token và UID cho đặt lại mật khẩu
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