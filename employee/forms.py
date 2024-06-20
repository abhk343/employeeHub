from django import forms
from .models import Employee, Overtime, Department
from datetime import datetime
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User, Group

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


class AttendanceForm(forms.Form):
    """
    Form for adding attendance records.
    """
    current_year = datetime.now().year
    years = [year for year in range(current_year - 1, current_year + 11)]  
    date = forms.DateField(widget=forms.SelectDateWidget(years=years))
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.CheckboxSelectMultiple)

class EmployeeCreateForm(forms.ModelForm):
    """
    Form for creating employee records.
    """
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
    """
    Form for adding overtime records.
    """
    class Meta:
        model = Overtime
        fields = ['Employee', 'Date', 'Overtime_hours', 'Overtime_minutes']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.Form):
    """
    Form for selecting a department.
    """
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Department')

class OvertimeFilterForm(forms.Form):
    """
    Form for filtering overtime records by department, month, and year.
    """
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Department')
    month = forms.IntegerField(min_value=1, max_value=12, label='Month')
    year = forms.IntegerField(min_value=1900, max_value=datetime.now().year + 1, label='Year')
