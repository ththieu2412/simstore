from django.db import models
from apps.accounts.models import Employee
from django.core.validators import RegexValidator

class MobileNetworkOperator(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'mobile_network_operator'

class Category1(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category_1'

class Category2(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category_2'

class SIM(models.Model):
    STATUS_CHOICES = [
        (0, 'Hết hàng'),
        (1, 'Có sẵn'),
        (2, 'Đang đăng bán'),
    ]

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{9,15}$', 'Số điện thoại không hợp lệ!')]
    )

    mobile_network_operator = models.ForeignKey(MobileNetworkOperator, on_delete=models.CASCADE)
    category_1 = models.ForeignKey(Category1, on_delete=models.CASCADE)
    category_2 = models.ForeignKey(Category2, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    export_price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1  
    )

    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.phone_number
    
    class Meta:
        db_table = 'sim'
