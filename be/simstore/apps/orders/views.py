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

                discount_instance = self._validate_discount(data.get("discount_code"))


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
        filters = {
            "status_order": self.request.query_params.get("status_order"),
            "customer__id": self.request.query_params.get("customer"),
            "discount__id": self.request.query_params.get("discount"),
            "ward": self.request.query_params.get("ward"),
            "sim__id": self.request.query_params.get("sim"),
        }
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        queryset = queryset.filter(**{k: v for k, v in filters.items() if v is not None})

        if start_date:
            try:
                queryset = queryset.filter(created_at__gte=start_date)
            except ValueError:
                raise ValueError("Ngày bắt đầu không hợp lệ. Định dạng phải là YYYY-MM-DD.")
        if end_date:
            try:
                queryset = queryset.filter(created_at__lte=end_date)
            except ValueError:
                raise ValueError("Ngày kết thúc không hợp lệ. Định dạng phải là YYYY-MM-DD.")

        return queryset
    
    def _get_or_create_customer(self, customer_data):
        if not customer_data:
            raise ValueError("Thiếu thông tin khách hàng")

        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            return customer_serializer.save()

        # Trả về lỗi đúng format nếu có lỗi validation
        raise ValueError(self._format_errors(customer_serializer.errors))

    # Helper function to format errors properly
    def _format_errors(self, errors):
        formatted_errors = []
        for field, error in errors.items():
            formatted_errors.append(f"{field}: {', '.join(error)}")
        return " ".join(formatted_errors)

    def _validate_discount(self, discount_code):
        if not discount_code:
            return None

        try:
            discount = Discount.objects.select_for_update().get(discount_code=discount_code)
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

        try:
            sim = SIM.objects.select_for_update().get(id=sim_id)
            if sim.status == 0: 
                raise ValueError("SIM đã được bán")
            elif sim.status == 1:  
                raise ValueError("SIM chưa được đăng bán và không thể sử dụng")
            return sim
        except SIM.DoesNotExist:
            raise ValueError("SIM không tồn tại")

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
        """Cập nhật đơn hàng và trả về toàn bộ kết quả đã cập nhật"""
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
                fields_to_update = ["detailed_address", "ward", "note", "discount", "customer"]
                for field in fields_to_update:
                    if field in data:
                        if field == "customer":
                            customer_data = data.get("customer")
                            if customer_data:
                                customer_serializer = CustomerSerializer(order.customer, data=customer_data, partial=True)
                                if customer_serializer.is_valid():
                                    customer_serializer.save()
                                else:
                                    raise ValueError(self._format_errors(customer_serializer.errors))
                        else:
                            setattr(order, field, data[field])

                if "discount" in data or "sim" in data:
                    order.total_price = order.calculate_total_price()

                order.save()

                serializer = self.get_serializer(order)
                return api_response(
                    status.HTTP_200_OK,
                    data=serializer.data,
                )

            except Exception as e:
                return api_response(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    errors=f"Lỗi trong quá trình cập nhật: {str(e)}",
                )

    def _update_order_status(self, order, data):
        """
        Cập nhật trạng thái đơn hàng với các kiểm tra bổ sung.
        """
        new_status = data.get("status_order", None)
        employee_id = data.get("employee_id")

        if not employee_id:
            raise ValueError("Cần cung cấp employee_id để cập nhật trạng thái.")

        employee = get_object_or_404(Employee, pk=employee_id)

        if employee.status == 0:  
            raise ValueError("Nhân viên đã nghỉ việc, không thể cập nhật trạng thái đơn hàng.")
        if not employee.account.is_active:  
            raise ValueError("Tài khoản của nhân viên đã bị vô hiệu hóa, không thể cập nhật trạng thái đơn hàng.")

        if order.status_order in [0, 3]: 
            raise ValueError("Không thể cập nhật trạng thái đơn hàng đã hủy hoặc đã giao thành công.")

        if new_status is not None and new_status != order.status_order:
            if new_status == 0:
                order.sim.status = 2
                order.sim.save()

            DetailUpdateOrder.objects.create(
                order=order,
                status_updated=new_status,
                employee=employee,
                updated_at=now(),
            )

            if new_status == 3:
                Payment.objects.filter(order=order).update(status=1)
            
            order.status_order = new_status

    def destroy(self, request, *args, **kwargs):
        """Xóa đơn hàng nếu trạng thái là 'Chờ xác nhận'"""
        order = self.get_object()

        if order.status_order != 1: 
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Chỉ có thể xóa đơn hàng ở trạng thái 'Chờ xác nhận'."
            )
        
        order.sim.status = 2
        order.sim.save()

        self.perform_destroy(order)
        return api_response(
            status.HTTP_204_NO_CONTENT,
            data="Đơn hàng đã được xóa thành công."
        )

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