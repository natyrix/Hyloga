# Generated by Django 3.0.3 on 2020-08-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.TextField(),
        ),
    ]
