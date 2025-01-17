# Generated by Django 4.2.9 on 2024-06-12 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_employee_dol'),
        ('product', '0003_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='available_quantity',
        ),
        migrations.CreateModel(
            name='Stock_in',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField()),
                ('issue_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.item')),
            ],
        ),
    ]
