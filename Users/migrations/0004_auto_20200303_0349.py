# Generated by Django 3.0.3 on 2020-03-03 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20200219_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(choices=[('Bride', 'Bride'), ('Groom', 'Groom')], max_length=30),
        ),
    ]
