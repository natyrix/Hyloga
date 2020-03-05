from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

st = (
        ('Verified', 'Verified'),
        ('Unverified', 'Unverified')
    )


class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Vendor(models.Model):
    st = (
        ('Verified', 'Verified'),
        ('Unverified', 'Unverified')
    )
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='vendor_images/', default='vendor_images/default-logo.png')
    slug = models.SlugField(max_length=30, null=True, blank=True)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    address = models.CharField(max_length=100)
    status = models.CharField(choices=st, max_length=30)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    login_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VendorImage(models.Model):
    image_location = models.ImageField(upload_to='vendor_images/', blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor.name


class Pricing(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    value = models.FloatField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class Logos(models.Model):
    logo = models.ImageField(upload_to='vendor_images/', default='vendor_images/default-logo.png')


def slug_generator(sender, instance, *args, **kwargs):
    uname = instance.email.split('@')
    instance.slug = str(uname[0]).strip()


pre_save.connect(slug_generator, sender=Vendor)
