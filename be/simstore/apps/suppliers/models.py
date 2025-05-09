from django.db import models
from apps.simcards.models import SIM
from apps.accounts.models import Employee

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    status = models.BooleanField(default=True) 

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'supplier'


class ImportReceipt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='importReceipt')  # ID nhân viên tạo hóa đơn

    def __str__(self):
        return f"Import Receipt {self.id} from {self.supplier.name}"
    
    class Meta:
        db_table = 'import_receipt'


class ImportReceiptDetail(models.Model):
    import_receipt = models.ForeignKey(ImportReceipt, on_delete=models.CASCADE)
    sim = models.ForeignKey(SIM, on_delete=models.CASCADE, related_name='importReceiptDetail')
    import_price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Receipt {self.import_receipt.id} - SIM {self.sim.id}"

    class Meta:
        db_table = 'import_receipt_detail'
        constraints = [
            models.UniqueConstraint(fields=['import_receipt', 'sim'], name='unique_import_sim')
        ]
