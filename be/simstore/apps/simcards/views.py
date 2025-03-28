from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MobileNetworkOperator, Category1, Category2, SIM
from .serializers import MobileNetworkOperatorSerializer, Category1Serializer, Category2Serializer, SimSerializer
from django.utils.timezone import now
from rest_framework.decorators import action

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

class SimViewSet(BaseViewSet):
    queryset = SIM.objects.all()
    serializer_class = SimSerializer

    def update(self, request, *args, **kwargs):
        """Cập nhật SIM (Chỉ cập nhật khi status khác 0)"""
        instance = self.get_object()

        if instance.status == 0:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Không thể cật nhật SIM đã hết hàng"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Tự động lọc theo query params (nếu có)
        """
        queryset = super().get_queryset()
        
        # Lọc theo status
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        
        # Lọc theo mobile_network_operator
        mobile_network_operator = self.request.query_params.get('mobile_network_operator')
        if mobile_network_operator is not None:
            queryset = queryset.filter(mobile_network_operator=mobile_network_operator)
        
        # Lọc theo khoảng giá
        min_price = self.request.query_params.get('min_price')
        if min_price is not None:
            queryset = queryset.filter(export_price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price')
        if max_price is not None:
            queryset = queryset.filter(export_price__lte=max_price)
        
        return queryset
