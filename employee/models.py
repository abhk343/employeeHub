from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

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
    Punch_Card_NO = models.IntegerField(unique=True)
    Name = models.CharField(max_length=25)
    Designation = models.CharField(max_length=30)
    Location = models.CharField(max_length=30)
    DOB = models.DateField()
    DOJ = models.DateField()
    DOL = models.DateField(null=True)
    Parents_Name = models.CharField(max_length=25)
    Martial_Status = models.CharField(max_length=25)
    Permanent_Address = models.TextField()
    Present_Address = models.TextField()
    Blood_Group = models.CharField(max_length=10)
    UAN_Number = models.IntegerField(null=True, unique=True)
    PF_PW = models.IntegerField()
    ESI_Number = models.IntegerField()
    Mobile_No = models.IntegerField()
    Email = models.EmailField(null=True)
    Aadhar_No = models.IntegerField()
    PAN = models.CharField(max_length=25)
    Bank_Acc_NO = models.IntegerField()
    IFSC_Code = models.CharField(max_length=25)
    Bank_Name = models.CharField(max_length=25)
    Emergency_Contact_No = models.IntegerField()
    Contact_No = models.IntegerField()
    Sur_name = models.CharField(max_length=25)
    Qualification = models.CharField(max_length=25)
    Experience = models.CharField(max_length=25)
    Remarks = models.TextField()
    Salary = models.IntegerField()

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
