# Generated by Django 3.0.3 on 2020-08-23 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0011_vendor_last_logout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='last_logout',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]