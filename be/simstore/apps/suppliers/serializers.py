from rest_framework import serializers
from .models import Supplier, ImportReceipt, SIM, ImportReceiptDetail
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

class SIMCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIM
        fields = ['phone_number', 'mobile_network_operator', 'category_1', 'category_2', 'employee', 'status']

        

class ImportReceiptDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportReceiptDetail
        fields = ['import_receipt', 'sim', 'import_price']

class SIMCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIM
        fields = ['phone_number', 'mobile_network_operator', 'category_1', 'category_2', 'employee', 'status']

class ImportReceiptSerializer(serializers.ModelSerializer):
    sim_list = SIMCreateSerializer(many=True, write_only=True)  # Danh sách SIM nhận vào
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = ImportReceipt
        fields = ['id', 'created_at', 'note', 'supplier', 'employee', 'sim_list', 'supplier_name', 'employee_name']
        read_only_fields = ['created_at']

    def validate_sim_list(self, sim_list):
        """
        Kiểm tra trùng lặp phone_number trước khi tạo SIM mới.
        """
        # Lấy danh sách phone_number từ sim_list
        phone_numbers = [sim['phone_number'] for sim in sim_list]

        # Kiểm tra trùng lặp trong dữ liệu gửi lên
        if len(phone_numbers) != len(set(phone_numbers)):
            raise serializers.ValidationError("Danh sách SIM có số điện thoại trùng lặp.")

        # Kiểm tra phone_number đã tồn tại trong DB chưa
        existing_phones = SIM.objects.filter(phone_number__in=phone_numbers).values_list('phone_number', flat=True)
        if existing_phones:
            raise serializers.ValidationError(f"Các số điện thoại sau đã tồn tại: {', '.join(existing_phones)}")

        return sim_list

    def create(self, validated_data):
        """
        Tạo ImportReceipt, tạo SIM và ghi vào ImportReceiptDetail.
        """
        sim_data = validated_data.pop('sim_list', [])  # Lấy danh sách SIM
        import_receipt = ImportReceipt.objects.create(**validated_data)  # Tạo phiếu nhập

        for sim_info in sim_data:
            sim = SIM.objects.create(**sim_info)  # Tạo SIM mới
            ImportReceiptDetail.objects.create(
                import_receipt=import_receipt,
                sim=sim,
                import_price=sim_info.get('import_price', 0)  # Lấy giá nhập
            )

        return import_receipt

