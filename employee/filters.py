# filters.py
import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    Department = django_filters.CharFilter(field_name='Department__Department_Name', lookup_expr='icontains')
    Name = django_filters.CharFilter(lookup_expr='icontains')
    Designation = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['Name', 'Department', 'Designation']
