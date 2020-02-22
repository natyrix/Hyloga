from django.db import models
from Vendor.models import Vendor
from Users.models import Users
from datetime import datetime


class Chat(models.Model):
    sent_time = models.DateTimeField(default=datetime.now)
    message = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
