# Generated by Django 3.0.3 on 2020-08-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RateandReview', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rate_value',
            field=models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]),
        ),
    ]
