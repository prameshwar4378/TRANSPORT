# Generated by Django 5.1 on 2025-01-19 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0002_remove_customuser_business_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='business_name',
            field=models.CharField(max_length=100),
        ),
    ]
