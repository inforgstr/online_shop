# Generated by Django 4.2.5 on 2023-10-22 10:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shop_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='about',
            field=ckeditor.fields.RichTextField(verbose_name='About page content'),
        ),
    ]
