from django.urls import path
from .views import *

urlpatterns = [
    
    path("",home,name='home'),
    # Department URLs
    path('dept/', DepartmentListView.as_view(), name='department_list'),
    path('create/', DepartmentCreateView.as_view(), name='department_create'),
    path('update/<int:pk>/', DepartmentUpdateView.as_view(), name='department_update'),
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
    
    # Employee URLs
    path('emp/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Attendance URLs
    path('attcreate/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('lecount/', monthly_absence_count, name='monthly_absence_count'),
    
    # Overtime URLs
    path('otcrte/', OvertimeCreateView.as_view(), name='overtime_add'),
    path('otlist/', OvertimeListView.as_view(), name='overtime_list'),
]
