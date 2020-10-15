from django.db import models
from Vendor.models import Vendor
from Users.models import Users
from django.utils import timezone

sender = (
        ('Vendor', 'Vendor'),
        ('Users', 'Users')
    )


class Chat(models.Model):
    sent_time = models.DateTimeField(default=timezone.now, editable=False)
    message = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    sender = models.CharField(choices=sender, max_length=10, blank=True)
    read_status = models.BooleanField(default=False)
