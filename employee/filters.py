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