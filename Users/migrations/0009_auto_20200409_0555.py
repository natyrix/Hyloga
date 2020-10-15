# Generated by Django 3.0.3 on 2020-04-09 05:55

import Users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_auto_20200409_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersimage',
            name='image_location',
            field=models.ImageField(upload_to='user_photos/', validators=[Users.validators.validate_file_size]),
        ),
    ]