# Generated by Django 4.2.9 on 2024-07-16 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_purchase_date_product_invoice_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Price_per_peice',
            new_name='Price_per_piece',
        ),
    ]