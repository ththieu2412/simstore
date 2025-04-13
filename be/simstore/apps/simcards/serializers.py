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

class MobileNetworkOperatorMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNetworkOperator
        fields = ['id', 'name']

class SimSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    mobile_network_operator = MobileNetworkOperatorMinimalSerializer()  
    category_1 = Category1Serializer()  
    category_2 = Category2Serializer()  
    employee = serializers.SerializerMethodField()  

    class Meta:
        model = SIM
        fields = '__all__'

    def get_updated_at(self, obj):
        """Chuyển đổi định dạng ngày tháng"""
        return obj.updated_at.strftime("%d/%m/%Y %H:%M:%S") if obj.updated_at else None

    def get_employee(self, obj):
        """Trả về thông tin nhân viên hoặc None nếu không có"""
        if obj.employee:
            return {
                "id": obj.employee.id,
                "full_name": obj.employee.full_name
            }
        return None  # Trả về None nếu không có nhân viên

    def validate_phone_number(self, value):
        """Kiểm tra số điện thoại đã tồn tại chưa"""
        if SIM.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("SIM với số điện thoại này đã tồn tại.")
        return value

class SimListSerializer(serializers.ModelSerializer):
    mobile_network_operator = MobileNetworkOperatorMinimalSerializer()  

    class Meta:
        model = SIM
        fields = ['id', 'phone_number', 'status', 'export_price', 'mobile_network_operator']
