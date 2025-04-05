from django.db import models
from apps.locations.models import Ward
from apps.simcards.models import SIM
from apps.accounts.models import Employee
from django.utils.timezone import now

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
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
    status = models.BooleanField(default=False)
    discount_code = models.CharField(max_length=50, blank=True)
    employee = models.ForeignKey(
        Employee,  
        on_delete=models.CASCADE, 
        related_name='discount_records'
    )

    def save(self, *args, **kwargs):
        date_str = now().strftime("%d%m%y")  # Lấy ngày tháng năm (DDMMYY)
        last_discount = Discount.objects.order_by('-id').first()  # Lấy ID lớn nhất
        next_id = last_discount.id + 1 if last_discount else 1  # ID tiếp theo
        self.discount_code = f"MGG{date_str}{next_id}"
        super().save(*args, **kwargs)

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

    status_order = models.IntegerField(choices=STATUS_CHOICES, default=1) 
    detailed_address = models.CharField(max_length=255)
    
    sim = models.ForeignKey(SIM, on_delete=models.CASCADE) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE) 
    discount = models.OneToOneField(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=500, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Order {self.id} for {self.customer.full_name}"
    
    class Meta:
        db_table = 'order'

    def calculate_total_price(self):
        """Tính tổng tiền đơn hàng dựa trên giá SIM và giảm giá."""
        total = self.sim.export_price
        if self.discount and self.discount.status:
            discount_amount = total * self.discount.percentage / 100
            total -= discount_amount
        return total

    def save(self, *args, **kwargs):
        """Ghi đè phương thức save để cập nhật total_price trước khi lưu vào database."""
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
    
class DetailUpdateOrder(models.Model):
    STATUS_CHOICES = [
        (0, 'Đã hủy'),
        (2, 'Đang giao hàng'),
        (3, 'Đã giao hàng'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    status_updated = models.IntegerField(choices=STATUS_CHOICES)
    employee = models.ForeignKey(
        Employee,  
        on_delete=models.CASCADE,  
        related_name='order_updates' 
    ) 

    def __str__(self):
        return f"Update for Order {self.order.id} at {self.updated_at}"

    class Meta:
        db_table = 'detail_update_order'
        ordering = ['-updated_at']

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('transfer', 'Chuyển khoản')
    ]

    STATUS_CHOICES = [
        (0, 'Chưa thanh toán'),
        (1, 'Đã thanh toán'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.get_payment_method_display()}"

    class Meta:
        db_table = 'payment'