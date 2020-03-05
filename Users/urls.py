from django.urls import path
from . import views
urlpatterns = [
    path('<slug:slug_txt>', views.home, name='users_home'),
    path('users_search/<int:id>', views.users_search, name='users_search'),
    path('<slug:slug_txt>/vendors', views.users_vendors, name='users_vendors'),
    path('users_vendor/<int:id>', views.users_vendor, name='users_vendor'),
]
