# Generated by Django 3.0.3 on 2020-04-12 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_usersimage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersimage',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
