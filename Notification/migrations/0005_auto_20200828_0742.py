# Generated by Django 3.0.3 on 2020-08-28 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0014_remove_vendor_last_logout'),
        ('Notification', '0004_auto_20200828_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Vendor.Vendor'),
        ),
    ]
