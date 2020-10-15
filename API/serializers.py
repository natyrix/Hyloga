from rest_framework import serializers

from Vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ['slug', 'status', 'login_id']
