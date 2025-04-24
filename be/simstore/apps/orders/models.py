from django.db import models
from apps.locations.models import Ward
from apps.simcards.models import SIM
from apps.accounts.models import Employee
from django.utils.timezone import now
from .constants import (
    ORDER_STATUS_CHOICES,
    DETAIL_UPDATE_STATUS_CHOICES,
    PAYMENT_STATUS_CHOICES,
    PAYMENT_METHOD_CHOICES,
    DISCOUNT_STATUS_CHOICES,
    DISCOUNT_STATUS_UNUSED
)

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "customer"


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(choices=DISCOUNT_STATUS_CHOICES, default=False)
    discount_code = models.CharField(max_length=50, blank=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="discount_records",
    )

    def __str__(self):
        return f"{self.percentage}% discount"

    class Meta:
        db_table = "discount"


class Order(models.Model):
    status_order = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    detailed_address = models.CharField(max_length=255)

    sim = models.ForeignKey(SIM, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    discount = models.OneToOneField(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=500, null=True, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.customer.full_name}"

    class Meta:
        db_table = "order"

    def calculate_total_price(self):
        """Tính tổng tiền đơn hàng dựa trên giá SIM và giảm giá."""
        total = self.sim.export_price
        if self.discount and not self.discount.status:
            discount_amount = total * self.discount.percentage / 100
            total -= discount_amount
        return total

    def save(self, *args, **kwargs):
        """Ghi đè phương thức save để cập nhật total_price trước khi lưu vào database."""
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
class DetailUpdateOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    status_updated = models.IntegerField(choices=DETAIL_UPDATE_STATUS_CHOICES)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="order_updates",
    )

    def __str__(self):
        return f"Update for Order {self.order.id} at {self.updated_at}"

    class Meta:
        db_table = "detail_update_order"
        ordering = ["-updated_at"]


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.get_payment_method_display()}"

    class Meta:
        db_table = "payment"