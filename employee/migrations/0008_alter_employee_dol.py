# Generated by Django 4.2.9 on 2024-06-10 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_remove_overtime_overtime_overtime_overtime_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='DOL',
            field=models.DateField(blank=True, null=True),
        ),
    ]