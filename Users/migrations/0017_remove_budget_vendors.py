# Generated by Django 3.0.3 on 2020-05-09 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0016_auto_20200429_0347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='vendors',
        ),
    ]
