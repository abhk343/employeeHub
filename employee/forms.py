from django import forms
from .models import Attendance, Employee, Department, Overtime
from django.contrib.auth.models import User, Group
from django.forms.widgets import SelectDateWidget
from datetime import datetime

class CustomUserCreationForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Assign Group")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user

# forms.py
from django import forms
from .models import Department

class DepartmentSelectForm(forms.Form):
    departments = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect,
        label="Departments"
    )

class AttendanceForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.none(), widget=forms.CheckboxSelectMultiple)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Attendance
        fields = ['date']

    def __init__(self, *args, **kwargs):
        employees_queryset = kwargs.pop('employees_queryset', None)
        super().__init__(*args, **kwargs)
        if employees_queryset is not None:
            self.fields['employees'].queryset = employees_queryset

    def save(self, commit=True):
        attendance = super().save(commit=False)
        if commit:
            attendance.save()
            self.save_m2m()  # Save the many-to-many relationships
        return attendance


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeCreateForm, self).__init__(*args, **kwargs)
        current_year = datetime.now().year
        years = [year for year in range(1900, current_year + 1)]
        self.fields['DOB'].widget = SelectDateWidget(years=years)
        self.fields['DOJ'].widget = SelectDateWidget(years=years)
        self.fields['DOL'].widget = SelectDateWidget(years=years)

class OvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = ['Employee', 'Date', 'Overtime_hours', 'Overtime_minutes']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Department')

class OvertimeFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Department')
    month = forms.IntegerField(min_value=1, max_value=12, label='Month')
    year = forms.IntegerField(min_value=1900, max_value=datetime.now().year + 1, label='Year')
