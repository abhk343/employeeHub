import django_filters
from .models import *

class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.ChoiceFilter(
        field_name='Department__Department_Name',
        choices=lambda: [(dept.Department_Name, dept.Department_Name) for dept in Department.objects.all().order_by('Department_Name')],
        empty_label='Select Department',
        label='Department'
    )
    name = django_filters.CharFilter(
        field_name='Name',
        lookup_expr='icontains',
        label='Name'
    )
    designation = django_filters.ChoiceFilter(
        field_name='Designation',
        choices=lambda: [(desig, desig) for desig in Employee.objects.values_list('Designation', flat=True).distinct().order_by('Designation')],
        empty_label='Select Designation',
        label='Designation'
    )

    class Meta:
        model = Employee
        fields = ['name', 'department', 'designation']

class AttendanceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='employee__Name',  # Use the related name lookup
        lookup_expr='icontains',
        label='Name'
    )
    designation = django_filters.ChoiceFilter(
        field_name='employee__Designation',  # Use the related name lookup
        choices=lambda: [(desig, desig) for desig in Employee.objects.values_list('Designation', flat=True).distinct().order_by('Designation')],
        empty_label='Select Designation',
        label='Designation'
    )

    class Meta:
        model = Attendance
        fields = ['name', 'designation']
        
        
import django_filters as filters
from django import forms
from .models import Attendance, Employee, Department

import django_filters
from .models import Employee

import django_filters
from .models import Attendance, Employee
import django_filters
from django import forms
from .models import Attendance, Employee, Department

class AttFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    
    name = django_filters.CharFilter(
        field_name='employee__Name',  # Use the related name lookup
        lookup_expr='icontains',
        label='Name'
    )
    
    department = django_filters.ModelChoiceFilter(
        field_name='employee__Department',  # Corrected field name to use ForeignKey field
        queryset=Department.objects.all(),
        label='Department'
    )

    designation = django_filters.ChoiceFilter(
        field_name='employee__Designation',  # Corrected field name to use CharField field
        choices=[(designation, designation) for designation in Employee.objects.values_list('Designation', flat=True).distinct()],
        label='Designation'
    )

    class Meta:
        model = Attendance
        fields = ['name', 'department', 'designation', 'start_date', 'end_date']


import django_filters
from django import forms
from .models import Overtime, Employee, Department

class OvertimeFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='Date', lookup_expr='gte', label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateFilter(field_name='Date', lookup_expr='lte', label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    
    name = django_filters.CharFilter(
        field_name='Employee__Name',  # Use the related name lookup
        lookup_expr='icontains',
        label='Name'
    )
    
    department = django_filters.ModelChoiceFilter(
        field_name='Employee__Department',  # Corrected field name to use ForeignKey field
        queryset=Department.objects.all(),
        label='Department'
    )

    designation = django_filters.ChoiceFilter(
        field_name='Employee__Designation',  # Corrected field name to use CharField field
        choices=[(designation, designation) for designation in Employee.objects.values_list('Designation', flat=True).distinct()],
        label='Designation'
    )

    class Meta:
        model = Overtime
        fields = ['name', 'department', 'designation', 'start_date', 'end_date']
