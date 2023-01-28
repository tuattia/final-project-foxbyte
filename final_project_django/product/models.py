from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    harga = models.IntegerField(default=1, validators=[MaxValueValidator(999999), MinValueValidator(1)])
    stock = models.IntegerField(default=0, validators=[MaxValueValidator(999), MinValueValidator(0)])

    class Meta:
        db_table = 'product'


class Transaksi(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.now(), blank=True)
    
    class Meta:
        db_table = 'transaksi'


class Quantity(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_product')
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE, related_name='related_transaksi')
    quantity = models.IntegerField(default=1, validators=[MaxValueValidator(999), MinValueValidator(1)])

    class Meta:
        db_table = 'quantity'
