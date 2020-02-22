from django.urls import path
from . import views

urlpatterns = [
    path('register_couple', views.registerCouple, name='register_couple'),
    path('register_vendor', views.registerVendor, name='register_vendor'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
