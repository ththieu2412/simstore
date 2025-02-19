from django.db import models
from apps.locations.models import Ward
from apps.simcards.models import SIM
from apps.accounts.models import Employee

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'customer'


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)  # True nếu còn hiệu lực
    employee = models.ForeignKey(
        Employee,  # Liên kết tới model Employee
        on_delete=models.CASCADE,  # Xóa bản ghi nếu nhân viên bị xóa
        related_name='created_records'  # Tạo quan hệ ngược
    )

    def __str__(self):
        return f"{self.percentage}% discount"
    
    class Meta:
        db_table = 'discount'


class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Đã hủy'),
        (1, 'Chờ xác nhận'),
        (2, 'Đang giao hàng'),
        (3, 'Đã giao hàng'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),  # Tiền mặt
        ('Bank Card', 'Bank Card'),  # Thẻ ngân hàng
    ]

    status_order = models.IntegerField(choices=STATUS_CHOICES, default=1) 
    payment_methods = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    detailed_address = models.CharField(max_length=255)
    
    sim = models.ForeignKey(SIM, on_delete=models.CASCADE) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE) 
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)  
    note = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Order {self.id} for {self.customer.full_name}"
    
    class Meta:
        db_table = 'order'
