# Generated by Django 3.0.3 on 2020-08-23 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0019_auto_20200514_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='last_logout',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]