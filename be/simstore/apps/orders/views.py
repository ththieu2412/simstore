from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from .models import Order, Customer, Discount
from .serializers import OrderSerializer, CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "put", "patch"]

    def create(self, request, *args, **kwargs):
        data = request.data

        # 1️⃣ Kiểm tra hoặc tạo mới khách hàng
        customer_data = data.get("customer", None)
        if not customer_data:
            return Response({"error": "Thiếu thông tin khách hàng"}, status=status.HTTP_400_BAD_REQUEST)

        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
        else:
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Kiểm tra mã giảm giá (nếu có)
        discount_id = data.get("discount")
        discount_instance = None
        if discount_id:
            try:
                discount_instance = Discount.objects.get(id=discount_id)
                if discount_instance.end_date < now() or not discount_instance.status:
                    return Response({"error": "Mã giảm giá không hợp lệ hoặc đã hết hạn"}, status=status.HTTP_400_BAD_REQUEST)
            except Discount.DoesNotExist:
                return Response({"error": "Mã giảm giá không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ["get", "put", "patch"]  # Chỉ cho phép xem (GET) và cập nhật (PUT/PATCH)

    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin khách hàng"""
        partial = kwargs.pop("partial", False)  # Hỗ trợ cả PUT (full update) và PATCH (partial update)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)