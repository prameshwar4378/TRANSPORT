# Generated by Django 5.1.1 on 2025-01-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0030_party_alternate_mobile_party_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
