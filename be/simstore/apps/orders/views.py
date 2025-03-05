from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from .models import Order, Customer, Discount
from .serializers import OrderSerializer, CustomerSerializer
from django.db import transaction

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
            with transaction.atomic():  # Bắt đầu transaction
                # 1️⃣ Kiểm tra hoặc tạo mới khách hàng
                customer_data = data.get("customer")
                if not customer_data:
                    raise ValueError("Thiếu thông tin khách hàng")

                customer_serializer = CustomerSerializer(data=customer_data)
                if customer_serializer.is_valid():
                    customer = customer_serializer.save()
                else:
                    raise ValueError(customer_serializer.errors)

                # 2️⃣ Kiểm tra mã giảm giá (nếu có)
                discount_id = data.get("discount")
                discount_instance = None
                if discount_id:
                    try:
                        discount_instance = Discount.objects.get(id=discount_id)
                        if discount_instance.end_date < now() or not discount_instance.status:
                            raise ValueError("Mã giảm giá không hợp lệ hoặc đã hết hạn")
                    except Discount.DoesNotExist:
                        raise ValueError("Mã giảm giá không tồn tại")

                # 3️⃣ Tạo đơn hàng mới
                order_data = {
                    "status_order": data["status_order"],
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
                    return format_response(status.HTTP_201_CREATED, data=order_serializer.data)
                else:
                    raise ValueError(order_serializer.errors)

        except ValueError as e:
            return format_response(status.HTTP_400_BAD_REQUEST, status_text="error", error_message=str(e))
        except Exception:
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