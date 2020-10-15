from django.db import models
from Vendor.models import Vendor
from Guest.models import Guest
from Users.models import Users


class Rate(models.Model):
    type = (
        ('Vendor', 'Vendor'),
        ('System', 'System')
    )
    rv = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rate_value = models.IntegerField(choices=rv)
    type = models.CharField(choices=type, max_length=10)
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.DO_NOTHING)
    guest = models.ForeignKey(Guest, blank=True, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, blank=True, null=True, on_delete=models.DO_NOTHING)


class Review(models.Model):
    type = (
        ('Vendor', 'Vendor'),
        ('System', 'System')
    )
    review = models.TextField()
    type = models.CharField(choices=type, max_length=10)
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.DO_NOTHING)
    guest = models.ForeignKey(Guest, blank=True, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, blank=True, null=True, on_delete=models.DO_NOTHING)
