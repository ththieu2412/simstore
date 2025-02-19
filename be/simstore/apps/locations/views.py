from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Province, District, Ward
from .serializers import ProvinceSerializer, DistrictSerializer, WardSerializer

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
