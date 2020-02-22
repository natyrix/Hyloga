from django.db import models
from django.contrib.auth.models import User


class Administrator(models.Model):
    gen = (
        ("M", "Male"),
        ("F", "Female")
    )

    gender = models.CharField(choices=gen, max_length=10)
    phonenumber = models.CharField(max_length=20)
    login_id = models.OneToOneField(User, on_delete=models.CASCADE)


