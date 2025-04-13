from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MobileNetworkOperator, Category1, Category2, SIM
from .serializers import MobileNetworkOperatorSerializer, Category1Serializer, Category2Serializer, SimListSerializer, SimSerializer
from django.utils.timezone import now
from rest_framework.decorators import action
from utils import api_response

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet để custom response format
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(status.HTTP_200_OK)

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
    serializer_class = SimSerializer  # Mặc định sử dụng SimSerializer

    def get_serializer_class(self):
        """Sử dụng SimListSerializer cho action 'list'"""
        if self.action == 'list':
            return SimListSerializer  # Sử dụng SimListSerializer khi gọi GET danh sách
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        """Cập nhật SIM (Chỉ cập nhật khi status khác 0)"""
        instance = self.get_object()

        if instance.status == 0:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Không thể cập nhật SIM đã hết hàng")
        
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

        # Lọc theo category_1
        category_1 = self.request.query_params.get('category_1')
        if category_1 is not None:
            queryset = queryset.filter(category_1=category_1)

        # Lọc theo category_2
        category_2 = self.request.query_params.get('category_2')
        if category_2 is not None:
            queryset = queryset.filter(category_2=category_2)

        # Lọc theo employee (id hoặc name)
        employee_id = self.request.query_params.get('employee_id')
        if employee_id is not None:
            queryset = queryset.filter(employee__id=employee_id)

        employee_name = self.request.query_params.get('employee_name')
        if employee_name is not None:
            queryset = queryset.filter(employee__full_name__icontains=employee_name)
        
        return queryset
