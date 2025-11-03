from django.db import models

# Create your models here.

class Category(models.Model):
    ct_id = models.AutoField(primary_key=True) 
    ct_name = models.CharField(max_length=100)
    ct_description = models.CharField(max_length=255, blank=True)
    ct_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.ct_name


class Product(models.Model):
    pdt_id = models.AutoField(primary_key=True)
    pdt_name = models.CharField(max_length=150)
    pdt_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    pdt_dis_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pdt_qty = models.IntegerField(default=0)
    ct = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', db_column='ct_id')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.pdt_name
