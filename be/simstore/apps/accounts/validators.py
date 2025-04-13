import re
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers


def validate_phone_number(value):
    """Kiểm tra số điện thoại hợp lệ (chỉ chứa số và độ dài từ 10-15 ký tự)"""
    if not re.match(r"^\d{10,15}$", value):
        raise serializers.ValidationError(
            "Số điện thoại không hợp lệ (phải từ 10 đến 15 chữ số)."
        )
    return value


def validate_citizen_id(value):
    """Kiểm tra xem citizen_id có đúng 12 ký tự không"""
    if len(value) != 12:
        raise serializers.ValidationError("CCCD bắt buộc 12 ký tự số.")
    return value


def validate_date_of_birth(value):
    """Kiểm tra ngày sinh hợp lệ (không tương lai, ít nhất 15 tuổi)"""
    today = timezone.now().date()
    min_birth_date = today - timedelta(days=15 * 365)

    if value > today:
        raise serializers.ValidationError("Ngày sinh không hợp lệ.")
    if value > min_birth_date:
        raise serializers.ValidationError("Nhân viên phải lớn hơn 15 tuổi.")
    return value


def validate_avatar(value):
    """Kiểm tra avatar là ảnh hợp lệ và dưới 5MB"""
    if value.size > 5 * 1024 * 1024:  # 5MB
        raise serializers.ValidationError("Kích thước ảnh phải nhỏ hơn 5MB.")
    return value


def validate_password(value):
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