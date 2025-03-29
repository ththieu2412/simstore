from rest_framework import serializers
from .models import MobileNetworkOperator, Category1, Category2, SIM

class MobileNetworkOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNetworkOperator
        fields = '__all__'

class Category1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category1
        fields = '__all__'

class Category2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category2
        fields = '__all__'

class SimSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = SIM
        fields = '__all__'

    
    def get_updated_at(self, obj):
            """Chuyển đổi định dạng ngày tháng"""
            return obj.updated_at.strftime("%d/%m/%Y %H:%M:%S") if obj.updated_at else None
    
    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại đã tồn tại chưa"""
        if SIM.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("SIM với số điện thoại này đã tồn tại.")
        return value
