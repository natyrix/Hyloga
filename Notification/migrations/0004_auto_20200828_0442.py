# Generated by Django 3.0.3 on 2020-08-28 04:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0003_notification_read_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]