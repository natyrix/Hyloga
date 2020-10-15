from django.db import models
from Vendor.models import Vendor
from Users.models import Users
from django.utils import timezone


class Booking(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.vendor.name


class Appointment(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    expired = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.vendor.name
