# Generated by Django 4.2.5 on 2023-10-30 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_rename_order_orderitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
