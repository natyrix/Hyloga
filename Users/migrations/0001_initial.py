# Generated by Django 3.0.3 on 2020-02-12 23:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('role', models.CharField(choices=[('Bride', 'bride'), ('Groom', 'groom')], max_length=30)),
                ('wedding_date', models.DateField(default=django.utils.timezone.now)),
                ('fiance_first_name', models.CharField(max_length=30)),
                ('fiance_last_name', models.CharField(max_length=30)),
                ('fiance_email', models.CharField(max_length=30)),
                ('login_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ticked', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='VideoGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_location', models.FileField(upload_to='draft_videos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='UsersVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_location', models.FileField(upload_to='user_videos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='UsersImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_location', models.ImageField(upload_to='user_photos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_location', models.ImageField(upload_to='draft_photos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField()),
                ('content', models.TextField()),
                ('date_and_time', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
    ]
