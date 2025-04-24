import urllib.parse
import hmac
import hashlib
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Case, When, IntegerField
from rest_framework.response import Response
from rest_framework import status, viewsets, serializers

from django.http import HttpResponseRedirect


from utils import api_response
from .models import Customer, DetailUpdateOrder, Discount, Employee, Order, Payment, SIM, Ward
from .serializers import (
    CustomerSerializer,
    DiscountSerializer,
    OrderSerializer,
    PaymentSerializer,
)
from .constants import (
    ORDER_STATUS_CANCELLED,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_COMPLETED,
    PAYMENT_STATUS_UNPAID,
    PAYMENT_STATUS_PAID,
    PAYMENT_STATUS_FAILED,
    PAYMENT_METHOD_CHOICES,
    SIM_STATUS_OUT_OF_STOCK,
    SIM_STATUS_LISTED,
    SIM_STATUS_AVAILABLE,
    DISCOUNT_STATUS_USED,
    EMPLOYEE_STATUS_INACTIVE,
)

from rest_framework.decorators import api_view

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer", "discount", "sim").all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Sắp xếp danh sách đơn hàng theo trạng thái:
        - Chờ xác nhận
        - Đang giao
        - Giao thành công
        - Đã hủy
        """
        queryset = super().get_queryset()

        # Thứ tự sắp xếp tùy chỉnh
        queryset = queryset.annotate(
            custom_order=Case(
                When(status_order=ORDER_STATUS_CONFIRMED, then=0),  
                When(status_order=ORDER_STATUS_COMPLETED, then=1),  
                When(status_order=PAYMENT_STATUS_PAID, then=2),     
                When(status_order=ORDER_STATUS_CANCELLED, then=3), 
                default=4,  # Mặc định
                output_field=IntegerField(),
            )
        ).order_by("custom_order", "-created_at")  # Sắp xếp theo custom_order và thời gian tạo mới nhất

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Tạo đơn hàng mới.
        """
        data = request.data
        try:
            with transaction.atomic():
                customer = self._get_or_create_customer(data.get("customer"))
                discount = self._validate_discount(data.get("discount_code"))
                sim = self._validate_sim(data.get("sim"))
                order = self._create_order(data, customer, discount)
                self._update_sim_and_discount(sim, discount)
                self._create_payment(order, data.get("payment"))
                return api_response(status.HTTP_201_CREATED, data=OrderSerializer(order).data)
        except serializers.ValidationError as e:
            return api_response(status.HTTP_400_BAD_REQUEST, errors=e.detail)
        except ValueError as e:
            return api_response(status.HTTP_400_BAD_REQUEST, errors=str(e))
        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging
            return api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, errors="Lỗi không xác định")

    def list(self, request, *args, **kwargs):
        """
        Lấy danh sách đơn hàng với các bộ lọc.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_response(status.HTTP_200_OK, data=serializer.data)

    def filter_queryset(self, queryset):
        """
        Áp dụng bộ lọc cho danh sách đơn hàng.
        """
        filters = {
            "status_order": self.request.query_params.get("status_order"),
            # "customer__id": self.request.query_params.get("customer"),
            "discount__id": self.request.query_params.get("discount"),
            "ward": self.request.query_params.get("ward"),
            "sim__id": self.request.query_params.get("sim"),
        }
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        customer_name = self.request.query_params.get("customer")  # Lấy tên khách hàng từ query params

        # Lọc theo các trường cụ thể
        queryset = queryset.filter(**{k: v for k, v in filters.items() if v is not None})

        # Lọc theo ngày
        if start_date:
            queryset = self._filter_by_date(queryset, "created_at__gte", start_date)
        if end_date:
            queryset = self._filter_by_date(queryset, "created_at__lte", end_date)

        # Lọc theo tên khách hàng
        if customer_name:
            queryset = queryset.filter(customer__full_name__icontains=customer_name)

        return queryset

    def _filter_by_date(self, queryset, field, date_value):
        """
        Lọc theo ngày.
        """
        try:
            return queryset.filter(**{field: date_value})
        except ValueError:
            raise ValueError(f"Ngày không hợp lệ. Định dạng phải là YYYY-MM-DD.")

    def _get_or_create_customer(self, customer_data):
        """
        Lấy hoặc tạo khách hàng mới.
        """
        if not customer_data:
            raise ValueError("Thiếu thông tin khách hàng")
        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            return customer_serializer.save()
        raise serializers.ValidationError(customer_serializer.errors)

    def _validate_discount(self, discount_code):
        """
        Kiểm tra mã giảm giá.
        """
        if not discount_code:
            return None
        try:
            discount = Discount.objects.select_for_update().get(discount_code=discount_code)
            if discount.status == DISCOUNT_STATUS_USED:
                raise ValueError("Mã giảm giá đã được sử dụng")
            if discount.end_date < now():
                raise ValueError("Mã giảm giá đã hết hạn")
            if discount.start_date > now():
                raise ValueError("Mã giảm giá chưa có hiệu lực")
            return discount
        except Discount.DoesNotExist:
            raise ValueError("Mã giảm giá không tồn tại")

    def _validate_sim(self, sim_id):
        """
        Kiểm tra SIM.
        """
        if not sim_id:
            raise ValueError("Thiếu thông tin SIM")
        try:
            sim = SIM.objects.select_for_update().get(id=sim_id)
            if sim.status == SIM_STATUS_OUT_OF_STOCK:
                raise ValueError("SIM đã được bán")
            if sim.status == SIM_STATUS_AVAILABLE:
                raise ValueError("SIM chưa được đăng bán")
            return sim
        except SIM.DoesNotExist:
            raise ValueError("SIM không tồn tại")

    def _create_order(self, data, customer, discount):
        """
        Tạo đơn hàng mới.
        """
        sim = SIM.objects.get(id=data["sim"])

        discount_percentage = discount.percentage if discount else 0
        discount_amount = (sim.export_price * discount_percentage) / 100

        total_price = round(sim.export_price - discount_amount, 2)

        order_data = {
            "detailed_address": data["detailed_address"],
            "sim": data["sim"],
            "customer": customer.id,
            "ward": data["ward"],
            "discount": discount.id if discount else None,
            "note": data.get("note", ""),
            "total_price": total_price,
        }
        
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            return order_serializer.save()
        raise ValueError(order_serializer.errors)

    def _update_sim_and_discount(self, sim, discount):
        """
        Cập nhật trạng thái SIM và mã giảm giá.
        """
        sim.status = SIM_STATUS_OUT_OF_STOCK  
        sim.save()
        if discount:
            discount.status = DISCOUNT_STATUS_USED  
            discount.save()

    def _create_payment(self, order, payment_method):
        """
        Tạo thanh toán cho đơn hàng.
        """
        if payment_method not in dict(PAYMENT_METHOD_CHOICES):
            raise ValueError("Phương thức thanh toán không hợp lệ.")

        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            status=PAYMENT_STATUS_UNPAID,  
        )

        if payment_method == "cash":
            payment.payment_method = "Tiền mặt"
            payment.save()

        elif payment_method in ["VNPAY"]:
            payment.payment_method = "VNPAY"
            self._process_online_payment(order, payment)

        return payment

    def _process_online_payment(self, order, payment):
        """
        Xử lý thanh toán trực tuyến.
        """

        try:
            print(f"Đang xử lý thanh toán trực tuyến cho đơn hàng {order.id}...")
            payment.status = PAYMENT_STATUS_PAID
            payment.save()
        except Exception as e:
            payment.status = PAYMENT_STATUS_FAILED
            payment.save()
            raise ValueError(f"Lỗi khi xử lý thanh toán trực tuyến: {str(e)}")

    def update(self, request, *args, **kwargs):
        """
        Cập nhật thông tin đơn hàng.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Kiểm tra trạng thái đơn hàng
        if instance.status_order == ORDER_STATUS_COMPLETED:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể cập nhật đơn hàng đã hoàn thành."
            )

        if instance.status_order == ORDER_STATUS_CANCELLED:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                errors="Không thể cập nhật đơn hàng đã bị hủy."
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            with transaction.atomic():
                # Lưu thông tin cập nhật
                updated_order = serializer.save()

                # Nếu trạng thái đơn hàng thay đổi, thêm bản ghi vào DetailUpdateOrder
                if "status_order" in serializer.validated_data:
                    employee_id = request.data.get("employee_id")
                    if not employee_id:
                        return api_response(
                            status.HTTP_400_BAD_REQUEST,
                            errors="Thiếu thông tin employee_id."
                        )

                    try:
                        employee = Employee.objects.get(id=employee_id)
                    except Employee.DoesNotExist:
                        return api_response(
                            status.HTTP_404_NOT_FOUND,
                            errors="Nhân viên không tồn tại."
                        )

                    if employee.status == EMPLOYEE_STATUS_INACTIVE:
                        return api_response(
                            status.HTTP_400_BAD_REQUEST,
                            errors="Nhân viên đã nghỉ việc, không thể cập nhật đơn hàng."
                        )

                    if not employee.account.is_active:
                        return api_response(
                            status.HTTP_400_BAD_REQUEST,
                            errors="Tài khoản của nhân viên đã bị vô hiệu hóa, không thể cập nhật đơn hàng."
                        )

                    DetailUpdateOrder.objects.create(
                        order=updated_order,
                        status_updated=serializer.validated_data["status_order"],
                        employee=employee
                    )
                    
                    if serializer.validated_data["status_order"] == ORDER_STATUS_COMPLETED:
                        payment = Payment.objects.filter(order=updated_order).first()
                        if payment and payment.status == PAYMENT_STATUS_UNPAID:
                            payment.status = PAYMENT_STATUS_PAID
                            payment.save()

                return api_response(status.HTTP_200_OK, data=serializer.data)

        return api_response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

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

        if payment.status == PAYMENT_STATUS_PAID:
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

@api_view(['POST'])
def create_payment(request):
    order_id = request.data.get('order_id')
    if not order_id:
        return api_response(status.HTTP_400_BAD_REQUEST, errors="Thiếu order_id")
    
    order = get_object_or_404(Order, id=order_id)
    sim = order.sim

    amount =  order.total_price * 100  

    order_desc = f"Thanh toán sim {sim.phone_number}"
    ip_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')

    vnp_params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': settings.VNPAY_TMN_CODE,
        'vnp_Amount': int(amount),
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': order_id,
        'vnp_OrderInfo': order_desc,
        'vnp_OrderType': 'telco',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': settings.VNPAY_RETURN_URL,
        'vnp_IpAddr': ip_addr,
        'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
    }

    vnp_params = dict(sorted(vnp_params.items()))
    query_string = urllib.parse.urlencode(vnp_params)
    hash_data = query_string.encode('utf-8')
    vnp_secure_hash = hmac.new(
        settings.VNPAY_HASH_SECRET.encode('utf-8'),
        hash_data,
        hashlib.sha512
    ).hexdigest()

    vnp_params['vnp_SecureHash'] = vnp_secure_hash
    vnpay_url = f"{settings.VNPAY_PAYMENT_URL}?{urllib.parse.urlencode(vnp_params)}"

    return api_response(status.HTTP_200_OK, data={"payment_url": vnpay_url})

@api_view(['GET'])
def payment_return(request):
    vnp_params = request.GET.dict()
    secure_hash = vnp_params.get('vnp_SecureHash')
    vnp_params.pop('vnp_SecureHash', None)

    vnp_params = dict(sorted(vnp_params.items()))
    query_string = urllib.parse.urlencode(vnp_params, doseq=True)
    
    hash_data = query_string.encode('utf-8')
    calculated_hash = hmac.new(
        settings.VNPAY_HASH_SECRET.encode('utf-8'),
        hash_data,
        hashlib.sha512
    ).hexdigest()

    order_id = vnp_params.get('vnp_TxnRef')
    response_code = vnp_params.get('vnp_ResponseCode')

    if not response_code:
        return api_response(status.HTTP_400_BAD_REQUEST, errors="Thiếu vnp_ResponseCode")

    if secure_hash == calculated_hash:
        try:
            if response_code == '00':
                order = Order.objects.get(id=order_id)
                Payment.objects.create(
                    order=order, 
                    payment_method="VNPAY",  
                    status=PAYMENT_STATUS_PAID
                )
                # return api_response(status.HTTP_200_OK, data={"message": "Thanh toán thành công", "order_id": order_id})
                return HttpResponseRedirect(f"http://localhost:3000/payment-return?order_id={order_id}&status=success")
            # else:
            #     # Xử lý lỗi khi thanh toán thất bại
            #     return api_response(
            #         status.HTTP_400_BAD_REQUEST,
            #         errors=f"Thanh toán thất bại: Mã lỗi {response_code}"
            #     )
            else:
                return HttpResponseRedirect(
                    f"http://localhost:3000/payment-return?order_id={order_id}&status=failed"
                )
        except Order.DoesNotExist:
            return api_response(status.HTTP_404_NOT_FOUND, errors="Đơn hàng không tồn tại")
    else:
        return api_response(status.HTTP_400_BAD_REQUEST, errors="Sai chữ ký (Invalid Signature)")

@api_view(['GET'])
def payment_ipn(request):
    vnp_params = request.GET.dict()
    secure_hash = vnp_params.get('vnp_SecureHash')
    vnp_params.pop('vnp_SecureHash', None)

    vnp_params = dict(sorted(vnp_params.items()))
    query_string = urllib.parse.urlencode(vnp_params)
    hash_data = query_string.encode('utf-8')
    calculated_hash = hmac.new(
        settings.VNPAY_HASH_SECRET.encode('utf-8'),
        hash_data,
        hashlib.sha512
    ).hexdigest()

    if secure_hash == calculated_hash:
        order_id = vnp_params.get('vnp_TxnRef')
        response_code = vnp_params.get('vnp_ResponseCode')
        try:
            order = Order.objects.get(id=order_id)
            if response_code == '00':
                # Tạo một Payment mới khi thanh toán thành công
                payment = Payment.objects.create(
                    order=order,
                    payment_method="VNPAY",  # Hoặc phương thức thanh toán của bạn
                    status=PAYMENT_STATUS_PAID,
                    # updated_at=timezone.now()
                )

                return api_response(status.HTTP_200_OK, data={"message": "Thanh toán thành công", "order_id": order_id})
            else:
                return api_response(status.HTTP_400_BAD_REQUEST, errors=f"Thanh toán thất bại: Mã lỗi {response_code}")
        except Payment.DoesNotExist:
            return api_response(status.HTTP_404_NOT_FOUND, errors="Đơn hàng không tồn tại")
    else:
        return api_response(status.HTTP_400_BAD_REQUEST, errors="Sai chữ ký (Invalid Signature)")

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