from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MobileNetworkOperator, Category1, Category2, SIM, Employee
from .serializers import MobileNetworkOperatorSerializer, Category1Serializer, Category2Serializer, SimListSerializer, SimSerializer, SimUpdateSerializer
from django.utils.timezone import now
from rest_framework.decorators import action
from utils import api_response
from django.db.models import Case, When, IntegerField

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
            return SimListSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return SimUpdateSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        """Cập nhật SIM (Chỉ cập nhật khi status khác 0 và nhân viên có trạng thái True)"""
        instance = self.get_object()

        # Kiểm tra trạng thái SIM
        if instance.status == 0:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Không thể cập nhật SIM đã hết hàng")

        # Kiểm tra sự tồn tại của employee_id trong request
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="Thiếu mã nhân viên cập nhật")

        # Kiểm tra kiểu dữ liệu của employee_id
        try:
            employee_id = int(employee_id)
        except ValueError:
            return api_response(status.HTTP_400_BAD_REQUEST, errors="employee_id phải là số nguyên")

        # Kiểm tra trạng thái của nhân viên
        try:
            employee = Employee.objects.get(id=employee_id)
            if not employee.status:
                return api_response(status.HTTP_400_BAD_REQUEST, errors="Nhân viên không hoạt động, không thể cập nhật SIM")
        except Employee.DoesNotExist:
            return api_response(status.HTTP_404_NOT_FOUND, errors="Nhân viên không tồn tại")

        # Cập nhật thông tin nhân viên cho SIM
        instance.employee = employee
        instance.save()

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        """
        Sắp xếp danh sách SIM theo trạng thái:
        - Đang hoạt động (1)
        - Đang chờ (2)
        - Hết hàng (0)
        """
        queryset = super().get_queryset()

        # Thứ tự sắp xếp tùy chỉnh
        queryset = queryset.annotate(
            custom_order=Case(
                When(status=1, then=0),  # Đang hoạt động
                When(status=2, then=1),  # Đang chờ
                When(status=0, then=2),  # Hết hàng
                default=3,  # Mặc định
                output_field=IntegerField(),
            )
        ).order_by("custom_order", "-updated_at")  # Sắp xếp theo custom_order và thời gian tạo mới nhất

        # Áp dụng các bộ lọc
        queryset = self.filter_by_status(queryset)
        queryset = self.filter_by_mobile_network_operator(queryset)
        queryset = self.filter_by_price_range(queryset)
        queryset = self.filter_by_category(queryset)
        queryset = self.filter_by_employee(queryset)
        queryset = self.filter_by_phone_number(queryset)
        queryset = self.apply_pagination(queryset)

        return queryset

    def filter_by_status(self, queryset):
        """Lọc theo status"""
        status = self.request.query_params.get('status')
        if status is not None:
            return queryset.filter(status=status)
        return queryset

    def filter_by_mobile_network_operator(self, queryset):
        """Lọc theo nhà mạng"""
        mobile_network_operator = self.request.query_params.get('mobile_network_operator')
        if mobile_network_operator is not None:
            return queryset.filter(mobile_network_operator=mobile_network_operator)
        return queryset

    def filter_by_price_range(self, queryset):
        """Lọc theo khoảng giá"""
        min_price = self.request.query_params.get('min_price')
        if min_price is not None:
            queryset = queryset.filter(export_price__gte=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price is not None:
            queryset = queryset.filter(export_price__lte=max_price)

        return queryset

    def filter_by_category(self, queryset):
        """Lọc theo category_1 và category_2"""
        category_1 = self.request.query_params.get('category_1')
        if category_1 is not None:
            queryset = queryset.filter(category_1=category_1)

        category_2 = self.request.query_params.get('category_2')
        if category_2 is not None:
            queryset = queryset.filter(category_2=category_2)

        return queryset

    def filter_by_employee(self, queryset):
        """Lọc theo employee (id hoặc name)"""
        employee_id = self.request.query_params.get('employee_id')
        if employee_id is not None:
            queryset = queryset.filter(employee__id=employee_id)

        employee_name = self.request.query_params.get('employee_name')
        if employee_name is not None:
            queryset = queryset.filter(employee__full_name__icontains=employee_name)

        return queryset

    def filter_by_phone_number(self, queryset):
        """Lọc theo phone_number"""
        phone_number = self.request.query_params.get('phone_number')
        if phone_number is not None:
            queryset = queryset.filter(phone_number__icontains=phone_number)
        return queryset
    
    def apply_pagination(self, queryset):
        """Áp dụng skip và limit"""
        skip = self.request.query_params.get('skip')
        limit = self.request.query_params.get('limit')

        if skip is not None:
            try:
                skip = int(skip)
                queryset = queryset[skip:]  
            except ValueError:
                pass 

        if limit is not None:
            try:
                limit = int(limit)
                queryset = queryset[:limit]  
            except ValueError:
                pass  

        return queryset
