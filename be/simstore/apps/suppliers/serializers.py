from rest_framework import serializers
from .models import Supplier, ImportReceipt, SIM, ImportReceiptDetail, Employee
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
        
class SIMSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIM
        fields = ['phone_number', 'mobile_network_operator', 'category_1', 'category_2', 'employee', 'status']

class ImportReceiptSIMSerializer(serializers.Serializer):
    sim = SIMSerializer()  # Chứa thông tin SIM
    import_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class SupplierMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name']
class ImportReceiptSerializer(serializers.ModelSerializer):
    sim_list = ImportReceiptSIMSerializer(many=True, write_only=True)  # Danh sách SIM và giá nhập
    supplier = SupplierMinimalSerializer()
    employee = EmployeeSerializer()
    class Meta:
        model = ImportReceipt
        fields = ['id', 'created_at', 'note', 'supplier', 'employee', 'sim_list']
        read_only_fields = ['created_at']

    def validate_sim_list(self, sim_list):
        """Kiểm tra trùng lặp số điện thoại"""
        phone_numbers = [sim_data['sim']['phone_number'] for sim_data in sim_list]

        # Kiểm tra trùng lặp trong danh sách gửi lên
        if len(phone_numbers) != len(set(phone_numbers)):
            raise serializers.ValidationError("Danh sách SIM có số điện thoại trùng lặp.")

        # Kiểm tra số điện thoại đã tồn tại trong DB chưa
        existing_phones = SIM.objects.filter(phone_number__in=phone_numbers).values_list('phone_number', flat=True)
        if existing_phones:
            raise serializers.ValidationError(f"Các số điện thoại sau đã tồn tại: {', '.join(existing_phones)}")

        return sim_list

    def create(self, validated_data):
        """Tạo ImportReceipt, tạo SIM và ghi vào ImportReceiptDetail"""
        sim_data_list = validated_data.pop('sim_list', [])  # Lấy danh sách SIM từ request
        import_receipt = ImportReceipt.objects.create(**validated_data)  # Tạo phiếu nhập

        for sim_data in sim_data_list:
            sim_info = sim_data['sim']  
            import_price = sim_data['import_price']  

            sim = SIM.objects.create(**sim_info) 
            ImportReceiptDetail.objects.create(
                import_receipt=import_receipt,
                sim=sim,
                import_price=import_price
            )

        return import_receipt


