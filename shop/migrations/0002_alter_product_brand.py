# Generated by Django 4.2.5 on 2023-10-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='brand_products', to='shop.productbrand'),
        ),
    ]