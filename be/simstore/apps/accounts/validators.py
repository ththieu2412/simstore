import re
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .constants import *

def validate_phone_number(value):
    if not re.match(PHONE_NUMBER_REGEX, value):
        raise serializers.ValidationError(PHONE_NUMBER_ERROR)
    return value


def validate_citizen_id(value):
    if len(value) != CITIZEN_ID_LENGTH:
        raise serializers.ValidationError(CITIZEN_ID_ERROR)
    return value


def validate_date_of_birth(value):
    today = timezone.now().date()
    min_birth_date = today - timedelta(days=MIN_AGE_YEARS * 365)

    if value > today:
        raise serializers.ValidationError(DATE_OF_BIRTH_ERROR_FUTURE)
    if value > min_birth_date:
        raise serializers.ValidationError(DATE_OF_BIRTH_ERROR_AGE)
    return value


def validate_avatar(value):
    if value.size > MAX_AVATAR_SIZE_MB * 1024 * 1024:
        raise serializers.ValidationError(AVATAR_SIZE_ERROR)
    return value


def validate_password(value):
    if len(value) < PASSWORD_MIN_LENGTH:
        raise serializers.ValidationError(PASSWORD_ERROR_LENGTH)
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError(PASSWORD_ERROR_DIGIT)
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError(PASSWORD_ERROR_UPPERCASE)
    if not any(char.islower() for char in value):
        raise serializers.ValidationError(PASSWORD_ERROR_LOWERCASE)
    if not any(char in SPECIAL_CHARACTERS for char in value):
        raise serializers.ValidationError(PASSWORD_ERROR_SPECIAL)
    return value