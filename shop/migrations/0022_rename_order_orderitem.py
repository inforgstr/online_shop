# Generated by Django 4.2.5 on 2023-10-30 15:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0021_remove_productstyle_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderItem',
        ),
    ]
