from rest_framework import status, viewsets

from utils import api_response
from .models import District, Province, Ward
from .serializers import DistrictSerializer, ProvinceSerializer, WardSerializer

class CustomViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(status.HTTP_204_NO_CONTENT)

    def get_filtered_queryset(self, filter_field, filter_value):
        """
        Tiện ích để lọc queryset theo trường cụ thể.
        """
        if not filter_value:
            return None, api_response(
                status.HTTP_400_BAD_REQUEST,
                errors=f"{filter_field} là bắt buộc",
            )
        return self.queryset.filter(**{filter_field: filter_value}), None


class ProvinceViewSet(CustomViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class DistrictViewSet(CustomViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def list(self, request, *args, **kwargs):
        """API lấy danh sách quận theo province_id"""
        province_id = request.GET.get("province_id")
        if province_id:
            districts, error_response = self.get_filtered_queryset("province_id", province_id)
            if error_response:
                return error_response
        else:
            districts = self.queryset 

        serializer = self.get_serializer(districts, many=True)
        return api_response(status.HTTP_200_OK, data=serializer.data)


class WardViewSet(CustomViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

    def list(self, request, *args, **kwargs):
        """API lấy danh sách phường dựa vào district_id"""
        district_id = request.GET.get("district_id")
        if district_id:
            wards, error_response = self.get_filtered_queryset("district_id", district_id)
            if error_response:
                return error_response
        else:
            wards = self.queryset 

        serializer = self.get_serializer(wards, many=True)
        return api_response(status.HTTP_200_OK, data=serializer.data)