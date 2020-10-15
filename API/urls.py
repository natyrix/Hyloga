from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from API.views import VendorViewSet

router = DefaultRouter()
router.register('vendors', VendorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


