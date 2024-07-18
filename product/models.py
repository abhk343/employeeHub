from django.db import models
from employee.models import *

class Item(models.Model):
    Item_id = models.AutoField(primary_key=True)
    Item_Name = models.CharField(unique = True ,max_length=20)

    class Meta:
        db_table = "Item"
    
    def __str__(self):
        return self.Item_Name
    
class Supplier(models.Model):
    Supplier_id = models.AutoField(primary_key=True)
    Supplier_Name = models.CharField( unique = True,max_length=30)

    class Meta:
        db_table = "Supplier"
    
    def __str__(self):
        return self.Supplier_Name
    

class Product(models.Model):
    Purchase_id = models.AutoField(primary_key=True)
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Price_per_piece = models.IntegerField()
    SGST = models.IntegerField(default=0)
    CGST = models.IntegerField(default=0)
    Invoice_amount=models.IntegerField(default=0)
    Invoice_Date = models.DateField()
    Invoice_Number = models.IntegerField()

    class Meta:
        db_table = "Product"
        
    def __str__(self):
        return f"{self.Item} from {self.Supplier}"

class Stock_in(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    Quantity = models.IntegerField()
    issue_date = models.DateField()