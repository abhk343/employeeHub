from django import forms
from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['Supplier_Name']
        
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'Invoice_Date': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from .models import Stock_in, Employee

class StockInForm(forms.ModelForm):
    class Meta:
        model = Stock_in
        fields = ['employee', 'item', 'Quantity', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'})
            }

        
    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if department_id:
            self.fields['employee'].queryset = Employee.objects.filter(Department_id=department_id)


# forms.py

from django import forms
from employee.models import Department

class DepartmentSelectForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
