# Generated by Django 3.0.3 on 2020-02-26 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0007_auto_20200220_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='logo',
            field=models.ImageField(default='vendor_images/default-logo.png', upload_to='vendor_images/'),
        ),
    ]
