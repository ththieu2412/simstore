from rest_framework import serializers
from .models import Supplier, Employee, ImportReceipt
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
 
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name']

class ImportReceiptSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()  
    employee_id = EmployeeSerializer()
    class Meta:
        model = ImportReceipt
        fields = '__all__'

    def to_representation(self, instance):
        """Ghi đè dữ liệu trả về"""
        data = super().to_representation(instance)
        data['created_at'] = instance.created_at.strftime('%d/%m/%Y %H:%M:%S')
        return data
    
    def validate_note(self, value):
        """Ghi chú không được chứa toàn khoảng trắng"""
        if value and value.strip() == "":
            raise serializers.ValidationError("Ghi chú không hợp lệ.")
        return value

    def validate_supplier(self, value):
        """Nhà cung cấp phải hợp lệ"""
        if not Supplier.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Nhà cung cấp không hợp lệ.")
        return value

    def validate_employee_id(self, value):
        """Nhân viên phải hợp lệ"""
        if not Employee.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Nhân viên không hợp lệ.")
        return value
