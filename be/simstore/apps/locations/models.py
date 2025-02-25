from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=255, db_collation='utf8mb4_bin')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'province'


class District(models.Model):
    name = models.CharField(max_length=255, db_collation='utf8mb4_bin')
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='districts')

    def __str__(self):
        return f"{self.name}, {self.province.name}"
    
    class Meta:
        db_table = 'district'


class Ward(models.Model):
    name = models.CharField(max_length=255, db_collation='utf8mb4_bin')
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='wards')

    def __str__(self):
        return f"{self.name}, {self.district.name}"
    
    class Meta:
        db_table = 'ward'
