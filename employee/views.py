from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum, F
from collections import defaultdict
import csv
from .models import Department, Employee, Attendance, Overtime
from .forms import EmployeeCreateForm, AttendanceForm, DepartmentForm, OvertimeForm, OvertimeFilterForm

@login_required
def home(request):
    return render(request, 'emp/home.html')

@login_required
def depemp_home(request):
    return render(request, 'emp/depemp_home.html')

@login_required
def attendance_home(request):
    return render(request, 'emp/attendance_home.html')

@login_required
def products_home(request):
    return render(request, 'emp/products_home.html')


# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'emp/dept_view.html'
    context_object_name = 'object_list'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['Department_Name']
    template_name = 'emp/dept_create.html'
    success_url = reverse_lazy('employee:department_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Department'
        return context

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ['Department_Name']
    template_name = 'emp/dept_create.html'
    success_url = reverse_lazy('employee:department_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Department'
        return context

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('department_list')

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of a department.
        """
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'Department deleted successfully'}, status=200)

# Employee Views
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'emp/emp_view.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(Name__icontains=query) | 
                Q(Designation__icontains=query) | 
                Q(Location__icontains=query)
            )
        return queryset

class EmployeeCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EmployeeCreateForm()
        return render(request, 'emp/emp_create.html', {'title': 'Create Employee', 'form': form})

    def post(self, request, *args, **kwargs):
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee:employee_list')
        return render(request, 'emp/emp_create.html', {'title': 'Create Employee', 'form': form})

class EmployeeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeCreateForm(instance=employee)
        return render(request, 'emp/emp_create.html', {'title': 'Update Employee', 'form': form})

    def post(self, request, pk, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeCreateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee:employee_list')
        return render(request, 'emp/emp_create.html', {'title': 'Update Employee', 'form': form})

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee_list')

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of an employee.
        """
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'Employee deleted successfully'}, status=200)

class ExportEmployeeDataView(View):
    def get(self, request):
        # Define the file name
        filename = "employee_data.csv"

        # Define the response content type
        response = HttpResponse(content_type='text/csv')

        # Set the header to force download
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Define the fields to include in the CSV
        field_names = [
            'Punch_Card_NO', 'Name', 'Designation', 'Location', 'DOB', 'DOJ', 'DOL', 'Parents_Name', 'Martial_Status', 
            'Permanent_Address', 'Present_Address', 'Blood_Group', 'UAN_Number', 'PF_PW', 'ESI_Number', 'Mobile_No', 
            'Email', 'Aadhar_No', 'PAN', 'Bank_Acc_NO', 'IFSC_Code', 'Bank_Name', 'Emergency_Contact_No', 'Contact_No', 
            'Sur_name', 'Qualification', 'Experience', 'Remarks', 'Salary',
        ]

        # Write header row
        writer.writerow(field_names)

        # Fetch all employees
        employees = Employee.objects.all()

        # Write data rows
        for employee in employees:
            row_data = [getattr(employee, field) for field in field_names]
            writer.writerow(row_data)

        return response

# Attendance Views
class AttendanceCreateView(LoginRequiredMixin, View):
    form_class = AttendanceForm
    template_name = 'emp/att_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            employees = form.cleaned_data['employees']
            # Save attendance records for selected employees
            for employee in employees:
                Attendance.objects.update_or_create(
                    employee=employee,
                    date=date,
                )
            return redirect('employee:monthly_absence_count')
        return render(request, self.template_name, {'form': form})

@login_required
def monthly_absence_count(request):
    selected_department = request.GET.get('department')
    selected_year = request.GET.get('year')
    
    if selected_year:
        try:
            selected_year = int(selected_year)
        except ValueError:
            selected_year = None
            
    absences = Attendance.objects.all()
    
    if selected_department:
        absences = absences.filter(employee__Department_id=selected_department)
        
    if selected_year:
        absences = absences.filter(date__year=selected_year)
        
    absence_data = absences.values('employee__Name', 'employee__Department__Department_Name', 'date__month').annotate(count=Count('attendance_id'))
    
    table_data = defaultdict(lambda: {'department': '', 'months': [0] * 12})
    
    for data in absence_data:
        employee_name = data['employee__Name']
        department_name = data['employee__Department__Department_Name']
        month = data['date__month'] - 1
        table_data[employee_name]['department'] = department_name
        table_data[employee_name]['months'][month] = data['count']
        
    context = {
        'departments': Department.objects.all(),
        'selected_department': selected_department,
        'selected_year': selected_year,
        'table_data': dict(table_data),
    }
    
    return render(request, 'emp/att_view.html', context)

# Overtime Views
class OvertimeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        department_form = DepartmentForm()
        overtime_form = OvertimeForm()
        return render(request, 'emp/ot_add.html', {
            'department_form': department_form,
            'overtime_form': overtime_form,
            'employees': Employee.objects.none()
        })

    def post(self, request):
        department_form = DepartmentForm(request.POST)
        overtime_form = OvertimeForm(request.POST)
        if 'filter' in request.POST and department_form.is_valid():
            department = department_form.cleaned_data['department']
            employees = Employee.objects.filter(Department=department)
            return render(request, 'emp/ot_add.html', {
                'department_form': department_form,
                'overtime_form': overtime_form,
                'employees': employees
            })
        if 'save' in request.POST and overtime_form.is_valid():
            overtime = overtime_form.save(commit=False)
            employee_id = request.POST.get('Employee')
            if employee_id:
                overtime.Employee = Employee.objects.get(pk=employee_id)
                if overtime.Overtime_hours > 8:
                    overtime.Overtime_hours = 8
                    overtime.Overtime_minutes = 0
                overtime.save()
                return redirect('overtime_list')
        employees = Employee.objects.filter(Department=department_form.cleaned_data['department']) if department_form.is_valid() else Employee.objects.none()
        return render(request, 'emp/ot_add.html', {
            'department_form': department_form,
            'overtime_form': overtime_form,
            'employees': employees
        })

class OvertimeListView(LoginRequiredMixin, View):
    def get(self, request):
        filter_form = OvertimeFilterForm()
        return render(request, 'emp/overtime_list.html', {
            'filter_form': filter_form,
            'overtimes': [],
            'department': None,
            'month': None,
            'year': None,
        })

    def post(self, request):
        filter_form = OvertimeFilterForm(request.POST)
        if filter_form.is_valid():
            department = filter_form.cleaned_data['department']
            month = filter_form.cleaned_data['month']
            year = filter_form.cleaned_data['year']
            overtimes = Overtime.objects.filter(
                Employee__Department=department,
                Date__month=month,
                Date__year=year
            ).values(
                'Employee__Name'
            ).annotate(
                total_minutes=Sum(F('Overtime_hours') * 60 + F('Overtime_minutes'))
            ).order_by('Employee__Name')
            for overtime in overtimes:
                overtime['total_hours'] = overtime['total_minutes'] // 60
                overtime['remaining_minutes'] = overtime['total_minutes'] % 60
            return render(request, 'emp/overtime_list.html', {
                'filter_form': filter_form,
                'overtimes': overtimes,
                'department': department,
                'month': month,
                'year': year,
            })
        return render(request, 'emp/overtime_list.html', {
            'filter_form': filter_form,
            'overtimes': [],
            'department': None,
            'month': None,
            'year': None,
        })
