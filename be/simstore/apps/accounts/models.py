from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.BooleanField(default=0)
    citizen_id = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'employee'

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = 'role'

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'account'
