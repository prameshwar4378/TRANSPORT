# Generated by Django 5.1 on 2025-01-20 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0016_remove_vehicleowner_vehicle_vehicle_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleowner',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Developer.business'),
        ),
    ]
