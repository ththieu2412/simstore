from django.db import models
from apps.accounts.models import Employee

class MobileNetworkOperator(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'mobileNetworkOperator'

class Category1(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category1'

class Category2(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category2'

class SIM(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    mobile_network_operator = models.ForeignKey(MobileNetworkOperator, on_delete=models.CASCADE)
    category_1 = models.ForeignKey(Category1, on_delete=models.CASCADE)
    category_2 = models.ForeignKey(Category2, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    export_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
    
    class Meta:
        db_table = 'sim'
