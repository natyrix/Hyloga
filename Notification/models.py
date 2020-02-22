from django.db import models
from Vendor.models import Vendor
from Users.models import Users
from datetime import datetime

ty = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Vendor', 'Vendor'),
    )


class Notification(models.Model):
    ty = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Vendor', 'Vendor'),
    )
    title = models.CharField(max_length=50)
    notification_date = models.DateTimeField(default=datetime.now)
    type = models.CharField(choices=ty, max_length=10)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


