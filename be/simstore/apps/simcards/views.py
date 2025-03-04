from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MobileNetworkOperator, Category1, Category2, SIM
from .serializers import MobileNetworkOperatorSerializer, Category1Serializer, Category2Serializer, SimSerializer

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet để custom response format
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "statuscode": status.HTTP_201_CREATED,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_201_CREATED)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)
        return Response({
            "statuscode": status.HTTP_400_BAD_REQUEST,
            "data": None,
            "status": "error",
            "errorMessage": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": None,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_200_OK)

class MobileNetworkOperatorViewSet(BaseViewSet):
    queryset = MobileNetworkOperator.objects.all()
    serializer_class = MobileNetworkOperatorSerializer

class Category1ViewSet(BaseViewSet):
    queryset = Category1.objects.all()
    serializer_class = Category1Serializer

class Category2ViewSet(BaseViewSet):
    queryset = Category2.objects.all()
    serializer_class = Category2Serializer

class SimViewSet(viewsets.ModelViewSet):
    queryset = SIM.objects.all()
    serializer_class = SimSerializer

    def destroy(self, request, *args, **kwargs):
        """Xóa SIM"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "statuscode": status.HTTP_204_NO_CONTENT,
            "data": None,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_204_NO_CONTENT)
