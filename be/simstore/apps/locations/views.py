from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Province, District, Ward
from .serializers import ProvinceSerializer, DistrictSerializer, WardSerializer
from rest_framework.views import APIView

class CustomViewSet(viewsets.ModelViewSet):
    """Custom ViewSet để chuẩn hóa format JSON trả về"""

    def format_response(self, statuscode, data=None, status_text="success", errorMessage=None):
        return Response({
            "statuscode": statuscode,
            "data": data,
            "status": status_text,
            "errorMessage": errorMessage
        }, status=statuscode)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.format_response(status.HTTP_200_OK, serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.format_response(status.HTTP_201_CREATED, serializer.data)
        return self.format_response(status.HTTP_400_BAD_REQUEST, None, "error", serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.format_response(status.HTTP_200_OK, serializer.data)
        return self.format_response(status.HTTP_400_BAD_REQUEST, None, "error", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.format_response(status.HTTP_204_NO_CONTENT, None)

class ProvinceViewSet(CustomViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet(CustomViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class WardViewSet(CustomViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

class DistrictViewSet(CustomViewSet):
    """
    API lấy danh sách quận theo province_id.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def list(self, request, *args, **kwargs):
        province_id = request.GET.get('province_id')

        if not province_id:
            return self.format_response(status.HTTP_400_BAD_REQUEST, None, "error", "province_id is required")

        districts = District.objects.filter(province_id=province_id)
        serializer = self.get_serializer(districts, many=True)
        return self.format_response(status.HTTP_200_OK, serializer.data)
    
class WardViewSet(CustomViewSet):
    """
    API lấy danh sách phường dựa vào district_id.
    """
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

    def list(self, request, *args, **kwargs):
        district_id = request.GET.get('district_id')

        if not district_id:
            return self.format_response(status.HTTP_400_BAD_REQUEST, None, "error", "district_id is required")

        wards = Ward.objects.filter(district_id=district_id)
        serializer = self.get_serializer(wards, many=True)
        return self.format_response(status.HTTP_200_OK, serializer.data)