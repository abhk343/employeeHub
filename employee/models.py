from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator , EmailValidator

class Department(models.Model):
    """
    Model to represent a department.
    """
    Department_id = models.AutoField(primary_key=True)
    Department_Name = models.CharField(max_length=25)

    class Meta:
        db_table = "Department"

    def __str__(self):
        return self.Department_Name

class Employee(models.Model):
    """
    Model to represent an employee.
    """
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Employee_id = models.AutoField(primary_key=True)
    Punch_Card_NO = models.CharField(unique=True, max_length=20)
    Name = models.CharField(max_length=25)
    Designation = models.CharField(max_length=30)
    Location = models.CharField(max_length=30)
    DOB = models.DateField()
    DOJ = models.DateField()
    DOL = models.DateField(null=True, blank=True)
    Parents_Name = models.CharField(max_length=25)
    
    # Changed Martial_Status to a boolean field
    Martial_Status = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    
    Permanent_Address = models.TextField()
    Present_Address = models.TextField()
    Blood_Group = models.CharField(max_length=10)
    UAN_Number = models.IntegerField(null=True, unique=True, validators=[MinValueValidator(1)])
    PF_PW = models.CharField(max_length=20)
    ESI_Number = models.IntegerField(validators=[MinValueValidator(1)])
    Mobile_No = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Email = models.EmailField(null=True, validators=[EmailValidator()])
    Aadhar_No = models.IntegerField(validators=[MinValueValidator(100000000000), MaxValueValidator(999999999999)])
    PAN = models.CharField(max_length=25)
    Bank_Acc_NO = models.IntegerField(validators=[MinValueValidator(1)])
    IFSC_Code = models.CharField(max_length=25)
    Bank_Name = models.CharField(max_length=25)
    Emergency_Contact_No = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Contact_No = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Sur_name = models.CharField(max_length=25)
    Qualification = models.CharField(max_length=25)
    Experience = models.CharField(max_length=25)
    Remarks = models.TextField()
    Salary = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "Employee"
        
    def __str__(self):
        return self.Name

class Attendance(models.Model):
    """
    Model to represent attendance records.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_id = models.AutoField(primary_key=True)
    date = models.DateField(default=date.today)  

    class Meta:
        db_table = "Attendance"

class Overtime(models.Model):
    """
    Model to represent overtime records.
    """
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Date = models.DateField()
    Overtime_hours = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(8)]
    )
    Overtime_minutes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(59)]
    )

    def clean(self):
        """
        Clean method to ensure overtime hours and minutes are within valid ranges.
        """
        total_minutes = self.Overtime_hours * 60 + self.Overtime_minutes
        if total_minutes > 8 * 60:
            self.Overtime_hours = 8
            self.Overtime_minutes = 0

    def save(self, *args, **kwargs):
        """
        Save method to ensure clean method is called before saving.
        """
        self.clean()  # Ensure the clean method is called
        super().save(*args, **kwargs)
