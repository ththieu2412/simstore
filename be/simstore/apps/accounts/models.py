from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.BooleanField(default=0)
    citizen_id = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'employee'

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True, db_collation='utf8mb4_bin')

    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = 'role'

class Account(AbstractUser):  # Kế thừa từ AbstractUser
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, blank=False)

    email = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    date_joined = None
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'account'
