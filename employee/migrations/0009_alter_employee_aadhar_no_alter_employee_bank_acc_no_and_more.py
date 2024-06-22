# Generated by Django 4.2.9 on 2024-06-21 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_employee_dol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Aadhar_No',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100000000000), django.core.validators.MaxValueValidator(999999999999)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Bank_Acc_NO',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Contact_No',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ESI_Number',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Email',
            field=models.EmailField(max_length=254, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Emergency_Contact_No',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Martial_Status',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Mobile_No',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='PF_PW',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Punch_Card_NO',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Salary',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='UAN_Number',
            field=models.IntegerField(null=True, unique=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]