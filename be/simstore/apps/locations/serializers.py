from rest_framework import serializers
from .models import Province, District, Ward

class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    # wards = serializers.StringRelatedField(many=True, read_only=True)
    # province_name = serializers.CharField(source='province.name', read_only=True)

    class Meta:
        model = District
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    district_id = serializers.PrimaryKeyRelatedField(source='district', read_only=True)
    province_id = serializers.PrimaryKeyRelatedField(source='district.province', read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'name', 'district_id', 'province_id']

