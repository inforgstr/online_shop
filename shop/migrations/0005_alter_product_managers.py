# Generated by Django 4.2.5 on 2023-10-16 11:20

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_productstyle_img'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('populars', django.db.models.manager.Manager()),
            ],
        ),
    ]
