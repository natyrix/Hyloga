from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import pre_save


class Users(models.Model):
    Role = (
      ('Bride',  'Bride'),
      ('Groom',  'Groom')
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30)
    role = models.CharField(choices=Role, max_length=30)
    wedding_date = models.DateField(default=timezone.now)
    fiance_first_name = models.CharField(max_length=30)
    fiance_last_name = models.CharField(max_length=30)
    fiance_email = models.EmailField(max_length=30)
    login_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " & " + self.fiance_first_name


class WishList(models.Model):
    is_ticked = models.BooleanField(default=False)
    content = models.CharField(max_length=50)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class CheckList(models.Model):
    order_number = models.IntegerField()
    content = models.TextField()
    date_and_time = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


class UsersVideo(models.Model):
    video_location = models.FileField(upload_to="user_videos/")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


class UsersImage(models.Model):
    image_location = models.ImageField(upload_to="user_photos/")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


class VideoGallery(models.Model):
    video_location = models.FileField(upload_to="draft_videos/")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


class ImageGallery(models.Model):
    image_location = models.ImageField(upload_to="draft_photos/")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


class Budget(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " & " + self.user.fiance_first_name


def slug_generator(sender, instance, *args, **kwargs):
    uname = instance.email.split('@')
    uname2 = instance.fiance_email.split('@')
    instance.slug = str(uname[0] + uname2[0]).strip()


pre_save.connect(slug_generator, sender=Users)
