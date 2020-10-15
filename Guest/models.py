from django.db import models
from Users.models import WishList, Users
from Vendor.models import Vendor


class Guest(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, blank=True)
    phonenumber = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name+' '+self.last_name


class TickedWishList(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)

    def __str__(self):
        return self.wishlist.content


class Invitation(models.Model):
    address = models.CharField(max_length=50)
    starttime = models.TimeField()
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)

