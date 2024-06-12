from django import forms
from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['Item_Name']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['Supplier_Name']
        
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['Item', 'Supplier', 'Quantity', 'Price', 'Purchase_Date', 'Invoice_Number']
        widgets = {
            'Purchase_Date': forms.DateInput(attrs={'type': 'date'}),
        }

        
class StockInForm(forms.ModelForm):
    class Meta:
        model = Stock_in
        fields = "__all__"
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }

from employee.models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['Department_Name'] 