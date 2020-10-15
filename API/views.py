from django.shortcuts import render
from rest_framework import viewsets

from API.serializers import VendorSerializer
from Vendor.models import Vendor
from rest_framework.permissions import AllowAny


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

