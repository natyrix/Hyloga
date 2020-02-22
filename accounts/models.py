from django.contrib.auth.models import User
from django.db import models

# Create your models here.

AcType = (
    ('Admin', 'Admin'),
    ('Vendor', 'Vendor'),
    ('Users', 'Users'),
)


class AccountType(models.Model):
    Actype = models.CharField(choices=AcType, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)