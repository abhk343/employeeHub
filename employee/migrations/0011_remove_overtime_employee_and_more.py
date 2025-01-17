# Generated by Django 4.2.9 on 2024-07-16 08:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_alter_department_department_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='overtime',
            name='Employee',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='Sur_name',
            new_name='Contact_Name',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='Salary',
            new_name='Gross1',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='Contact_No',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='PF_PW',
        ),
        migrations.AddField(
            model_name='employee',
            name='HRA',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='PF_Member_Id',
            field=models.CharField(default='0', max_length=25, validators=[django.core.validators.MinLengthValidator(25)]),
        ),
        migrations.AddField(
            model_name='employee',
            name='Relation',
            field=models.CharField(default='parent', max_length=25),
        ),
        migrations.AddField(
            model_name='employee',
            name='VDA',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='basic',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='convenience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='sp_convenience',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='Overtime',
        ),
    ]
