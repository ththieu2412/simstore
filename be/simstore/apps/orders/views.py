from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now

from rest_framework import status, viewsets

from utils import api_response
from .models import Customer, DetailUpdateOrder, Discount, Employee, Order, Payment, SIM
from .serializers import (
    CustomerSerializer,
    DiscountSerializer,
    OrderSerializer,
    PaymentSerializer,
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer", "discount", "sim").all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            with transaction.atomic():
                customer = self._get_or_create_customer(data.get("customer"))

                discount_instance = self._validate_discount(data.get("discount"))

                sim_instance = self._validate_sim(data.get("sim"))

                order = self._create_order(data, customer, discount_instance)

                self._update_sim_and_discount(sim_instance, discount_instance)

                self._create_payment(order, data.get("payment"))

                return api_response(status.HTTP_201_CREATED, data=OrderSerializer(order).data)

        except ValueError as e:
            return api_response(status.HTTP_400_BAD_REQUEST, errors=str(e))
        except Exception as e:
            return api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, errors="Lỗi không xác định")

    def list(self, request, *args, **kwargs):
        """
        Override list method to handle filtering of orders.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Return the filtered orders
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return api_response(status.HTTP_200_OK, data=serializer.data)
    
    def filter_queryset(self, queryset):
        """
        Apply filtering logic to the queryset based on URL parameters.
        """
        status_order = self.request.query_params.get("status_order", None)
        customer = self.request.query_params.get("customer", None)
        discount = self.request.query_params.get("discount", None)
        ward = self.request.query_params.get("ward", None)
        sim = self.request.query_params.get("sim", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        # Filter by status_order
        if status_order:
            queryset = queryset.filter(status_order=status_order)

        # Filter by customer
        if customer:
            queryset = queryset.filter(customer__id=customer)

        # Filter by discount
        if discount:
            queryset = queryset.filter(discount__id=discount)

        # Filter by ward
        if ward:
            queryset = queryset.filter(ward=ward)

        # Filter by sim
        if sim:
            queryset = queryset.filter(sim__id=sim)

        # Filter by start and end date
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset
    
    def _get_or_create_customer(self, customer_data):
        if not customer_data:
            raise ValueError("Thiếu thông tin khách hàng")

        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            return customer_serializer.save()
        raise ValueError(customer_serializer.errors)

    def _validate_discount(self, discount_id):
        if not discount_id:
            return None

        try:
            discount = Discount.objects.select_for_update().get(id=discount_id)
            if discount.status == 1:
                raise ValueError("Mã giảm giá đã được sử dụng")
            if discount.end_date < now():
                raise ValueError("Mã giảm giá đã hết hạn")
            if discount.start_date > now():
                raise ValueError("Mã giảm giá không hợp lệ")
            return discount
        except Discount.DoesNotExist:
            raise ValueError("Mã giảm giá không tồn tại")

    def _validate_sim(self, sim_id):
        if not sim_id:
            raise ValueError("Thiếu thông tin SIM")

        sim = SIM.objects.select_for_update().get(id=sim_id)
        if sim.status in [0, 1]:
            raise ValueError("SIM không hợp lệ")
        return sim

    def _create_order(self, data, customer, discount_instance):
        order_data = {
            "detailed_address": data["detailed_address"],
            "sim": data["sim"],
            "customer": customer.id,
            "ward": data["ward"],
            "discount": discount_instance.id if discount_instance else None,
            "note": data.get("note", ""),
        }
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            return order_serializer.save()
        raise ValueError(order_serializer.errors)

    def _update_sim_and_discount(self, sim_instance, discount_instance):
        sim_instance.status = 0 
        sim_instance.save()

        if discount_instance:
            discount_instance.status = 1  
            discount_instance.save()

    def _create_payment(self, order, payment_method):
        if payment_method not in dict(Payment.PAYMENT_METHOD_CHOICES):
            raise ValueError("Phương thức thanh toán không hợp lệ. Chỉ chấp nhận 'cash' hoặc 'tranfer'.")

        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            status=0,
        )

    def update(self, request, pk=None, *args, **kwargs):
        """Cập nhật đơn hàng"""
        order = get_object_or_404(Order, pk=pk)
        data = request.data.copy()

        if order.status_order in [0, 3]:  # 0: Đã hủy, 3: Đã giao thành công
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể cập nhật đơn hàng đã hủy hoặc đã giao thành công.",
            )

        with transaction.atomic():
            try:
                self._update_order_status(order, data)

                fields_to_update = ["detailed_address", "ward", "note", "discount"]
                for field in fields_to_update:
                    if field in data:
                        setattr(order, field, data[field])
                # Tính lại total_price nếu có thay đổi giảm giá
                if "discount" in data or "sim" in data:
                    order.total_price = order.calculate_total_price()

                order.save()

                return api_response(
                    status.HTTP_200_OK,
                    data={"order_id": order.id, "new_status": order.status_order},
                )

            except Exception as e:
                return api_response(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    errors=f"Lỗi trong quá trình cập nhật: {str(e)}",
                )

    def _update_order_status(self, order, data):
        new_status = data.get("status_order", None)
        if new_status is not None and new_status != order.status_order:
            employee_id = data.get("employee_id")
            if not employee_id:
                raise ValueError("Cần cung cấp employee_id để cập nhật trạng thái.")

            employee = get_object_or_404(Employee, pk=employee_id)
            DetailUpdateOrder.objects.create(
                order=order,
                status_updated=new_status,
                employee=employee,
                updated_at=now(),
            )
            order.status_order = new_status

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ["get", "put", "patch"] 

    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin khách hàng"""
        partial = kwargs.pop("partial", False)  
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_200_OK, data=serializer.data)

        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        """Lấy danh sách Payment, có thể lọc theo status hoặc phương thức thanh toán"""
        payments = self.queryset

        status_filter = request.query_params.get("status")
        if status_filter is not None:
            payments = payments.filter(status=status_filter)

        # Lọc theo phương thức thanh toán nếu có
        payment_method_filter = request.query_params.get("payment_method")
        if payment_method_filter:
            payments = payments.filter(payment_method=payment_method_filter)

        serializer = PaymentSerializer(payments, many=True)
        return api_response(status.HTTP_200_OK, data=serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        """Cập nhật Payment (trạng thái hoặc phương thức thanh toán)"""
        payment = get_object_or_404(Payment, pk=pk)

        if payment.status == 1:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể cập nhật Payment đã thanh toán.",
            )

        with transaction.atomic():
            data = request.data.copy()
            data["updated_at"] = timezone.now()  

            serializer = PaymentSerializer(payment, data=data, partial=kwargs.get("partial", False))
            if serializer.is_valid():
                serializer.save()
                return api_response(status.HTTP_200_OK, data=serializer.data)
            return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def create(self, request, *args, **kwargs):
        """Xử lý tạo mới bản ghi"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(status.HTTP_201_CREATED, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """Xử lý cập nhật bản ghi"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        if instance.status:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors={"status": "Không thể cập nhật khi khuyến mãi đã được sử dụng."},
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(status.HTTP_200_OK, data=serializer.data)
        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """Xóa bản ghi nhưng kiểm tra trước khi xóa"""
        instance = self.get_object()

        if instance.status:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors={"status": "Không thể xóa khi khuyến mãi đã được sử dụng."},
            )

        self.perform_destroy(instance)
        return api_response(status.HTTP_204_NO_CONTENT)