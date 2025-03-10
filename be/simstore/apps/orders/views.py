from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Order, Customer, Discount, Payment
from .serializers import OrderSerializer, CustomerSerializer, PaymentSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404

def format_response(status_code, data=None, status_text="success", error_message=""):
    """ Hàm chuẩn hóa response JSON """
    return Response({
        "statuscode": status_code,
        "data": data,
        "status": status_text,
        "errorMessage": error_message
    }, status=status_code)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "put", "patch"]

    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            with transaction.atomic():  
                #Kiểm tra hoặc tạo mới khách hàng
                customer_data = data.get("customer")
                if not customer_data:
                    raise ValueError("Thiếu thông tin khách hàng")

                customer_serializer = CustomerSerializer(data=customer_data)
                if customer_serializer.is_valid():
                    customer = customer_serializer.save()
                else:
                    raise ValueError(customer_serializer.errors)

                # Kiểm tra mã giảm giá
                discount_instance = None
                discount_id = data.get("discount")
                if discount_id:
                    try:
                        discount_instance = Discount.objects.select_for_update().get(id=discount_id)

                        if discount_instance.status == 0:
                            raise ValueError("Mã giảm giá đã được sử dụng")
                        if discount_instance.end_date < now():
                            raise ValueError("Mã giảm giá đã hết hạn")
                        if discount_instance.start_date > now():
                            raise ValueError("Mã giảm giá không hợp lệ")

                    except Discount.DoesNotExist:
                        raise ValueError("Mã giảm giá không tồn tại")

                #Tạo đơn hàng mới
                order_data = {
                    "detailed_address": data["detailed_address"],
                    "sim": data["sim"],
                    "customer": customer.id,  # Dùng ID khách hàng vừa tạo
                    "ward": data["ward"],
                    "discount": discount_instance.id if discount_instance else None,
                    "note": data.get("note", ""),
                }
                order_serializer = OrderSerializer(data=order_data)
                if order_serializer.is_valid():
                    order = order_serializer.save()

                    #Cập nhật trạng thái mã giảm giá
                    if discount_instance:
                        discount_instance.status = 0  # Đánh dấu là đã sử dụng
                        discount_instance.save()

                    payment_method = data.get("payment")
                    if payment_method not in dict(Payment.PAYMENT_METHOD_CHOICES):
                        raise ValueError("Phương thức thanh toán không hợp lệ. Chỉ chấp nhận 'cash' hoặc 'tranfer'.")
                    
                    payment = Payment.objects.create(
                        order = order,
                        payment_method = payment_method,
                        status = 0
                    )

                    return format_response(status.HTTP_201_CREATED, data=order_serializer.data)

                else:
                    raise ValueError(order_serializer.errors)

        except ValueError as e:
            return format_response(status.HTTP_400_BAD_REQUEST, status_text="error", error_message=str(e))
        except Exception as e:
            print(e)
            return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, status_text="error", error_message="Lỗi không xác định")

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ["get", "put", "patch"]  # Chỉ cho phép GET, PUT, PATCH

    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin khách hàng"""
        partial = kwargs.pop("partial", False)  # PUT (full update) hoặc PATCH (partial update)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return format_response(status.HTTP_200_OK, data=serializer.data)

        return format_response(status.HTTP_400_BAD_REQUEST, status_text="error", error_message=serializer.errors)
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()  # 
    serializer_class = PaymentSerializer

    def list(self, request):
        """Lấy danh sách Payment, có thể lọc theo status hoặc phương thức thanh toán."""
        payments = self.queryset  

        # Lọc theo status nếu có
        status_filter = request.query_params.get("status")
        if status_filter is not None:
            payments = payments.filter(status=status_filter)

        # Lọc theo phương thức thanh toán nếu có
        payment_method_filter = request.query_params.get("payment_method")
        if payment_method_filter:
            payments = payments.filter(payment_method=payment_method_filter)

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Cập nhật Payment (trạng thái hoặc phương thức thanh toán)"""
        payment = get_object_or_404(Payment, pk=pk)  

        with transaction.atomic():  
            serializer = PaymentSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return format_response(
                    status_code=status.HTTP_200_OK,
                    data=serializer.data,
                    status_text="success"
                )
            return format_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_text="error",
                error_message=serializer.errors
            )
