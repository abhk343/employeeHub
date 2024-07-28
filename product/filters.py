import django_filters
from .models import Product
from employee.models import *
from django.forms.widgets import DateInput
class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='Price_per_piece', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='Price_per_piece', lookup_expr='lte')
    purchase_date_min = django_filters.DateFilter(field_name='Invoice_Date', lookup_expr='gte',widget=DateInput(attrs={'type': 'date'}))
    purchase_date_max = django_filters.DateFilter(field_name='Invoice_Date', lookup_expr='lte',widget=DateInput(attrs={'type': 'date'}))
    item_name = django_filters.CharFilter(field_name='Item__Item_Name', lookup_expr='icontains', label='Item Name contains:')
    supplier_name = django_filters.CharFilter(field_name='Supplier__Supplier_Name', lookup_expr='icontains', label='Supplier Name contains:')    
    
    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'purchase_date_min', 'purchase_date_max', 'item_name', 'supplier_name']


import django_filters
from .models import Stock_in
from employee.models import Employee, Department  # Adjust based on your actual app structure

class StockFilter(django_filters.FilterSet):
    date_min = django_filters.DateFilter(field_name='issue_date', lookup_expr='gte',widget=DateInput(attrs={'type': 'date'}))
    date_max = django_filters.DateFilter(field_name='issue_date', lookup_expr='lte',widget=DateInput(attrs={'type': 'date'}))
    item_name = django_filters.CharFilter(field_name='Item__Item_Name', lookup_expr='icontains', label='Item Name contains:')
    employee = django_filters.CharFilter(field_name='employee__Emp_code', lookup_expr='icontains')
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        field_name='employee__department',
        label='Department'
    )

    class Meta:
        model = Stock_in
        fields = ['date_min', 'date_max', 'item_name', 'employee', 'department']

# filters.py
# filters.py
# employee/filters.py
import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    department = django_filters.CharFilter(lookup_expr='icontains')
    designation = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['name', 'department', 'designation']
