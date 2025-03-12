from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Order, Customer, Discount, Payment, SIM, Employee, DetailUpdateOrder
from .serializers import OrderSerializer, CustomerSerializer, PaymentSerializer, DiscountSerializer
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
                
                # Kiểm tra SIM trước khi tạo đơn hàng
                sim_instance = SIM.objects.select_for_update().get(id=data["sim"])
                if sim_instance.status in [0, 1]:  # 0: Hết hàng, 1: Có sẵn
                    raise ValueError("SIM không hợp lệ")

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

                    # Cập nhật trạng thái SIM về 0 (hết hàng)
                    sim_instance = SIM.objects.select_for_update().get(id=data["sim"])
                    sim_instance.status = 0
                    sim_instance.save()

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

    def update(self, request, pk=None, *args, **kwargs):
        """Cập nhật đơn hàng """
        order = get_object_or_404(Order, pk=pk)
        data = request.data.copy()
        employee_id = data.get("employee_id", None)

        #Không cho phép cập nhật nếu đơn hàng đã hủy
        if order.status_order == 0:
            return format_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_text="error",
                error_message="Không thể cập nhật đơn hàng đã hủy."
            )
        
        if order.status_order == 3:
            return format_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_text="error",
                error_message="Không thể cập nhật đơn hàng đã giao thành công."
            )

        #Lưu trạng thái cũ trước khi cập nhật
        old_status = order.status_order  
        new_status = data.get("status_order", None)

        with transaction.atomic():
            try:
                if new_status is not None and new_status != old_status:
                    if employee_id is None:
                        return format_response(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            status_text="error",
                            error_message="Cần cung cấp employee_id để cập nhật trạng thái."
                        )
                    
                    employee = get_object_or_404(Employee, pk=employee_id)
                    DetailUpdateOrder.objects.create(
                        order=order,
                        status_updated=new_status,
                        employee=employee,
                        updated_at=timezone.now()
                    )
                    order.status_order = new_status

                #Cập nhật các trường khác
                fields_to_update = ["detailed_address", "ward", "note", "discount"]
                for field in fields_to_update:
                    if field in data:
                        setattr(order, field, data[field])

                #Tính lại total_price nếu có thay đổi giảm giá
                if "discount" in data or "sim" in data:
                    order.total_price = order.calculate_total_price()
                    
                order.save()

                #Trả về response chuẩn
                return format_response(
                    status_code=status.HTTP_200_OK,
                    status_text="success",
                    data={"order_id": order.id, "new_status": order.status_order}
                )

            except Exception as e:
                return format_response(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    status_text="error",
                    error_message=f"Lỗi trong quá trình cập nhật: {str(e)}"
                )

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

    def update(self, request, pk=None, *args, **kwargs):
        """Cập nhật Payment (trạng thái hoặc phương thức thanh toán)"""
        payment = get_object_or_404(Payment, pk=pk)  

        # Không cho phép cập nhật nếu status đã là 1 (đã thanh toán)
        if payment.status == 1:
            return format_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_text="error",
                error_message="Không thể cập nhật Payment đã thanh toán."
            )

        with transaction.atomic():  
            data = request.data.copy()
            data["updated_at"] = timezone.now()  # Gán lại thời gian hiện tại

            serializer = PaymentSerializer(payment, data=data, partial=kwargs.get("partial", False))
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


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    # permission_classes = [IsAuthenticated]  # Chỉ cho phép người dùng đã đăng nhập truy cập

    def perform_create(self, serializer):
        # Có thể thêm logic xử lý trước khi tạo
        serializer.save()