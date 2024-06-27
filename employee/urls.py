from . import views
from django.urls import path
from .views import *

app_name = "employee"

urlpatterns = [
    # Home
    path('', home, name='home'),
    path('create_user/', create_user, name='create_user'),
    path('user1/', user1_view, name='HR'),
    path('user2/', user2_view, name='Supervisor'),
    path('depemp_home/', depemp_home, name='depemp_home'),
    path('attendance_home/', attendance_home, name='attendance_home'),
    path('products_home/', products_home, name='products_home'),

    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/update/<int:pk>/', DepartmentUpdateView.as_view(), name='department_update'),

    # Employee URLs
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('export-employee-data/', ExportEmployeeDataView.as_view(), name='export_employee_data'),
    
    # Attendance URLs
    path('attendance/select-department/', DepartmentSelectView.as_view(), name='select_department'),
    path('attendance/create/<int:department_id>/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/sele-dept/', DepartmentSelect.as_view(), name='sele_dept'),
    path('attendance/monthly-absence-count/', views.monthly_absence_count, name='monthly_absence_count'),
    # Overtime URLs
    path('overtime/create/', OvertimeCreateView.as_view(), name='overtime_add'),
    path('overtime/list/', OvertimeListView.as_view(), name='overtime_list'),
]
