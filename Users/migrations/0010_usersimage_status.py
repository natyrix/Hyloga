# Generated by Django 3.0.3 on 2020-04-12 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_auto_20200409_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersimage',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
