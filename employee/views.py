from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum, F
from collections import defaultdict
from django.contrib import messages
import csv
import logging
from .models import *
from django_filters.views import FilterView
from .filters import *
from .forms import *

logger = logging.getLogger(__name__)

# Views implementation will go here


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee:home')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    return render(request, 'emp/create_user.html', {'form': form})

def is_user1(user):
    return user.groups.filter(name='HR').exists()

def is_user2(user):
    return user.groups.filter(name='Supervisor').exists()

@login_required
@user_passes_test(is_user1)
def user1_view(request):
    return render(request, 'user1_view.html')

@login_required
@user_passes_test(is_user2)
def user2_view(request):
    return render(request, 'user2_view.html')


@login_required
def home(request):
    return render(request, 'emp/home.html')
    



@login_required
def depemp_home(request):
    return render(request, 'emp/depemp_home.html')

# @login_required
# def attendance_home(request):
#     return render(request, 'emp/attendance_home.html')

@login_required
def products_home(request):
    return render(request, 'emp/products_home.html')

def admin_check(user):
    return user.is_superuser

is_user1_required = user_passes_test(is_user1)

# Department Views

class DepartmentListView(LoginRequiredMixin, ListView):
    try:
        model = Department
        template_name = 'emp/dept_view.html'
        context_object_name = 'object_list'
    except Exception as e:
         render("error.html")
        
class DepartmentCreateView(LoginRequiredMixin, CreateView):
    try:
        model = Department
        fields = ['Department_Name']
        template_name = 'emp/dept_create.html'
        success_url = reverse_lazy('employee:department_list')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Create Department'
            return context
    except Exception as e:
         render("error.html")
        
class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    try:
        model = Department
        fields = ['Department_Name']
        template_name = 'emp/dept_create.html'
        success_url = reverse_lazy('employee:department_list')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Update Department'
            return context
    except Exception as e:
         render("error.html")
        
class EmployeeListView(LoginRequiredMixin, FilterView): 
    try:
        model = Employee
        template_name = 'emp/emp_view.html'
        context_object_name = 'employees'
        paginate_by = 5  # Number of employees per page
        filterset_class = EmployeeFilter

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Get the filtered queryset
            filtered_qs = self.get_queryset()
            
            # Calculate the total number of pages
            num_pages = (filtered_qs.count() // self.paginate_by) + (1 if filtered_qs.count() % self.paginate_by > 0 else 0)
            
            # Get the current page number
            page_number = int(self.request.GET.get('page', 1))
            
            # Adjust employees queryset to display only for current page
            start_index = (page_number - 1) * self.paginate_by
            end_index = start_index + self.paginate_by
            context['employees'] = filtered_qs[start_index:end_index]
            
            # Pass additional context variables
            context['current_page'] = page_number
            context['num_pages'] = num_pages
            
            # Fetch all departments and add to context
            context['departments'] = Department.objects.all()
            
            # Add the selected department and filter to the context
            context['selected_department'] = self.request.GET.get('Department', '')
            context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
            
            return context

        def get_queryset(self):
            queryset = super().get_queryset()
            
            # Apply the filter
            filter = self.filterset_class(self.request.GET, queryset=queryset)
            return filter.qs
    except Exception as e:
         render("error.html")
        
class EmployeeDetailView(LoginRequiredMixin, DetailView):
    try:
        model = Employee
        template_name = 'emp/emp_detail.html'
        context_object_name = 'employee'
    except Exception as e:
         render("error.html")
        

logger = logging.getLogger(__name__)

class EmployeeCreateView(LoginRequiredMixin, View):
    try:
        def get(self, request, *args, **kwargs):
            form = EmployeeCreateForm()
            return render(request, 'emp/emp_create.html', {'title': 'Create Employee', 'form': form})

        def post(self, request, *args, **kwargs):
            form = EmployeeCreateForm(request.POST,request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Employee created successfully!')
                    return redirect('employee:employee_list')
                except Exception as e:
                    logger.error(f"Error creating employee: {e}")
                    messages.error(request, 'There was an error creating the employee. Please try again.')
            else:
                logger.error(f"Form errors: {form.errors}")
                messages.error(request, 'Please correct the errors below.')
            return render(request, 'emp/emp_create.html', {'title': 'Create Employee', 'form': form})
    except Exception as e:
         render("error.html")
        
class EmployeeUpdateView(LoginRequiredMixin, View):
    try:
        def get(self, request, pk, *args, **kwargs):
            employee = get_object_or_404(Employee, pk=pk)
            form = EmployeeCreateForm(instance=employee)

            return render(request, 'emp/emp_create.html', {'edit': True, 'form': form})

        def post(self, request, pk, *args, **kwargs):

            employee = get_object_or_404(Employee, pk=pk)
            form = EmployeeCreateForm(request.POST, request.FILES,instance=employee)
            if form.is_valid():
                try:
                    # Check if Punch_Card_NO or UAN_Number has changed
                    if form.cleaned_data['Punch_Card_NO'] != employee.Punch_Card_NO:
                        employee.Punch_Card_NO = form.cleaned_data['Punch_Card_NO']
                    if form.cleaned_data['UAN_Number'] != employee.UAN_Number:
                        employee.UAN_Number = form.cleaned_data['UAN_Number']
                    employee.save()
                    return redirect('employee:employee_list')
                except IntegrityError:
                    # Handle specific integrity errors here
                    form.add_error(None, 'Employee with this Punch Card NO or UAN Number already exists.')
            
            # If form is not valid or errors occurred, render the form again with errors
            return render(request, 'emp/emp_create.html', {'edit': True, 'form': form})
    except Exception as e:
         render("error.html")
        
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    try:
        model = Employee
        success_url = reverse_lazy('employee:employee_list')

        def delete(self, request, *args, **kwargs):
            """
            Handle the deletion of an employee.
            """
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'message': 'Employee deleted successfully'}, status=200)
    except Exception as e:
         render("error.html")
        
class ExportEmployeeDataView(View):
    try:
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
                    'Department', 'Emp_code','Esic_no', 'Punch_Card_NO', 'Name', 'Designation', 'Location', 'DOB', 'DOJ', 'DOL', 'Parents_Name',
                    'Martial_Status', 'Permanent_Address', 'Present_Address', 'Blood_Group', 'UAN_Number', 'PF_Member_Id', 'ESI_Number', 
                    'Mobile_No', 'Email', 'Aadhar_No', 'PAN', 'Bank_Acc_NO', 'IFSC_Code', 'Bank_Name', 'Emergency_Contact_No', 
                    'Contact_Name', 'Relation', 'Qualification', 'Experience', 'basic', 'VDA', 'HRA', 'convenience', 'sp_convenience', 
                    'Gross1', 'Remarks'
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
    except Exception as e:
         render("error.html")
        



# class DepartmentSelectView(LoginRequiredMixin, View):
#     try:
#         template_name = 'emp/select_department.html'

#         def get(self, request, *args, **kwargs):
#             form = DepartmentSelectForm()
#             return render(request, self.template_name, {'form': form})

#         def post(self, request, *args, **kwargs):
#             form = DepartmentSelectForm(request.POST)
#             if form.is_valid():
#                 department = form.cleaned_data['departments']  # Access the selected department
#                 department_id = department.Department_id  # Get the Department_id of the selected department
#                 return redirect('employee:attendance_create', department_id=department_id)
#             return render(request, self.template_name, {'form': form})
#     except Exception as e:
#          render("error.html")
        


# class AttendanceCreateView(LoginRequiredMixin, View):
#     try:
#         template_name = 'emp/att_add.html'
#         form_class = AttendanceForm

#         def get_form(self, department_id=None):
#             if department_id is not None:
#                 employees = Employee.objects.filter(Department_id=department_id)
#             else:
#                 employees = Employee.objects.none()

#             form = self.form_class(employees_queryset=employees)
#             return form

#         def get(self, request, *args, **kwargs):
#             department_id = kwargs.get('department_id')
#             form = self.get_form(department_id)
#             return render(request, self.template_name, {'form': form, 'department_id': department_id})

#         def post(self, request, *args, **kwargs):
#             department_id = kwargs.get('department_id')
#             form = self.form_class(request.POST, employees_queryset=Employee.objects.filter(Department_id=department_id))

#             if form.is_valid():
#                 date = form.cleaned_data['date']
#                 selected_employees = form.cleaned_data['employees']

#                 for employee in selected_employees:
#                     Attendance.objects.update_or_create(
#                         employee=employee,
#                         date=date,
#                     )
#                 return redirect('employee:sele_dept')

#             return render(request, self.template_name, {'form': form, 'department_id': department_id})
#     except Exception as e:
#          render("error.html")


# class DepartmentSelect(LoginRequiredMixin, View):
#     try:
#         template_name = 'emp/sele_dept.html'

#         def get(self, request, *args, **kwargs):
#             departments = Department.objects.all()
#             selected_department = request.GET.get('department')
#             selected_year = request.GET.get('year')
#             context = {
#                 'departments': departments,
#                 'selected_department': selected_department,
#                 'selected_year': selected_year,
#             }
#             return render(request, self.template_name, context)

#         def post(self, request, *args, **kwargs):
#             # Assuming post is not needed as you are using GET method for the form
#             return redirect('employee:monthly_absence_count', department=request.POST.get('department'), year=request.POST.get('year'))
#     except Exception as e:
#          render("error.html")

# @login_required
# def monthly_absence_count(request):
#     try:
#         selected_department = request.GET.get('department')
#         selected_year = request.GET.get('year')
        
#         # Validate the year parameter
#         if selected_year:
#             try:
#                 selected_year = int(selected_year)
#             except ValueError:
#                 selected_year = None
                
#         absences = Attendance.objects.all()
        
#         # Apply filtering based on selected department and year
#         if selected_department:
#             absences = absences.filter(employee__Department_id=selected_department)
            
#         if selected_year:
#             absences = absences.filter(date__year=selected_year)
            
#         # Apply the AttendanceFilter
#         attendance_filter = AttendanceFilter(request.GET, queryset=absences)
#         absences = attendance_filter.qs

#         absence_data = absences.values('employee__Name', 'employee__Department__Department_Name', 'employee__Designation', 'date__month').annotate(count=Count('attendance_id'))
        
#         table_data = {}
        
#         for data in absence_data:
#             employee_name = data['employee__Name']
#             department_name = data['employee__Department__Department_Name']
#             designation = data['employee__Designation']
#             month = data['date__month'] - 1
            
#             if employee_name not in table_data:
#                 table_data[employee_name] = {
#                     'department': department_name,
#                     'designation': designation,
#                     'months': [0] * 12,
#                 }
            
#             table_data[employee_name]['months'][month] = data['count']
            
#         # Convert defaultdict to regular dictionary
#         table_data = dict(table_data)
        
#         # Convert dictionary items to list of tuples
#         table_data_list = list(table_data.items())
        
#         # Pagination
#         paginator = Paginator(table_data_list, 5)  # Show 10 items per page
#         page_number = request.GET.get('page')
        
#         try:
#             page_obj = paginator.page(page_number)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages if paginator.num_pages > 1 else 1)
        
#         context = {
#             'departments': Department.objects.all(),
#             'selected_department': selected_department,
#             'selected_year': selected_year,
#             'page_obj': page_obj,  # Pass paginated data to the template
#             'filter': attendance_filter,  # Pass the filter to template
#         }
        
#         return render(request, 'emp/att_view.html', context)
#     except Exception as e:
#         return render(request,"error.html")

# class AttendanceListView(ListView):
#     try:
#         model = Attendance
#         filterset_class = AttFilter
#         template_name = 'emp/att_list.html'  # Ensure this matches your template path
#         context_object_name = 'attendances'
#         paginate_by = 10  # Number of records per page

#         def get_queryset(self):
#             queryset = super().get_queryset()
#             self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
#             return self.filterset.qs

#         def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             context['filter'] = self.filterset
#             return context
#     except Exception as e:
#          render("error.html")

# class AttendanceDeleteView(DeleteView):
#     try:
            
#         model = Attendance
#         success_url = reverse_lazy('employee:attendance_list')

#         def delete(self, request, *args, **kwargs):
#             """
#             Handle the deletion of an attendance record via Ajax.
#             """
#             self.object = self.get_object()
#             try:
#                 self.object.delete()
#                 return JsonResponse({'message': 'Attendance record deleted successfully'}, status=200)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#     except Exception as e:
#          render("error.html")

# # Overtime Views
# class OvertimeCreateView(LoginRequiredMixin, View):
#     try:
#         def get(self, request):
#             department_form = DepartmentForm()
#             overtime_form = OvertimeForm()
#             return render(request, 'emp/ot_add.html', {
#                 'department_form': department_form,
#                 'overtime_form': overtime_form,
#                 'employees': Employee.objects.none()
#             })

#         def post(self, request):
#             department_form = DepartmentForm(request.POST)
#             overtime_form = OvertimeForm(request.POST)
#             if 'filter' in request.POST and department_form.is_valid():
#                 department = department_form.cleaned_data['department']
#                 employees = Employee.objects.filter(Department=department)
#                 return render(request, 'emp/ot_add.html', {
#                     'department_form': department_form,
#                     'overtime_form': overtime_form,
#                     'employees': employees
#                 })
#             if 'save' in request.POST and overtime_form.is_valid():
#                 overtime = overtime_form.save(commit=False)
#                 employee_id = request.POST.get('Employee')
#                 if employee_id:
#                     overtime.Employee = Employee.objects.get(pk=employee_id)
#                     if overtime.Overtime_hours > 8:
#                         overtime.Overtime_hours = 8
#                         overtime.Overtime_minutes = 0
#                     overtime.save()
#                     return redirect('employee:overtim_list')
#             employees = Employee.objects.filter(Department=department_form.cleaned_data['department']) if department_form.is_valid() else Employee.objects.none()
#             return render(request, 'emp/ot_add.html', {
#                 'department_form': department_form,
#                 'overtime_form': overtime_form,
#                 'employees': employees
#             })
#     except Exception as e:
#          render("error.html")
    
# class OvertimeListView(LoginRequiredMixin, View):
#     try:
            
#         def get(self, request):
#             filter_form = OvertimeFilterForm()
#             return render(request, 'emp/overtime_list.html', {
#                 'filter_form': filter_form,
#                 'overtimes': [],
#                 'department': None,
#                 'month': None,
#                 'year': None,
#             })

#         def post(self, request):
#             filter_form = OvertimeFilterForm(request.POST)
#             if filter_form.is_valid():
#                 department = filter_form.cleaned_data['department']
#                 month = filter_form.cleaned_data['month']
#                 year = filter_form.cleaned_data['year']
#                 overtimes = Overtime.objects.filter(
#                     Employee__Department=department,
#                     Date__month=month,
#                     Date__year=year
#                 ).values(
#                     'Employee__Name'
#                 ).annotate(
#                     total_minutes=Sum(F('Overtime_hours') * 60 + F('Overtime_minutes'))
#                 ).order_by('Employee__Name')
#                 for overtime in overtimes:
#                     overtime['total_hours'] = overtime['total_minutes'] // 60
#                     overtime['remaining_minutes'] = overtime['total_minutes'] % 60
#                 return render(request, 'emp/overtime_list.html', {
#                     'filter_form': filter_form,
#                     'overtimes': overtimes,
#                     'department': department,
#                     'month': month,
#                     'year': year,
#                 })
#             return render(request, 'emp/overtime_list.html', {
#                 'filter_form': filter_form,
#                 'overtimes': [],
#                 'department': None,
#                 'month': None,
#                 'year': None,
#             })
#     except Exception as e:
#          render("error.html")


# class OvertimeView(FilterView):
#     """
#     Displays a list of Overtime entries with filtering and pagination.
#     """
#     try:
#         model = Overtime
#         template_name = 'emp/ot_detaillist.html'
#         context_object_name = 'overtimes'
#         filterset_class = OvertimeFilter
#         paginate_by = 10  # Number of items per page

#         def get_context_data(self, **kwargs):
#             """
#             Adds pagination to the filtered queryset.
#             """
#             context = super().get_context_data(**kwargs)
#             filter = context['filter']
#             paginator = Paginator(filter.qs, self.paginate_by)
#             page_number = self.request.GET.get('page')
#             page_obj = paginator.get_page(page_number)
#             context['overtimes'] = page_obj
#             return context
#     except Exception as e:
#          render("error.html")
    
# class OvertimeDeleteView(View):
#     """
#     Handles the deletion of an overtime record via an Ajax request.
#     """
#     try:
            
#         def delete(self, request, overtime_id):
#             """
#             Deletes an overtime record.
#             """
#             overtime = get_object_or_404(Overtime, pk=overtime_id)

#             try:
#                 overtime.delete()
#                 return JsonResponse({'message': 'Overtime record deleted successfully.'}, status=204)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#     except Exception as e:
#          render("error.html")