from django.urls import path
from . import views
urlpatterns = [
    path('<slug:slug_txt>', views.dashboard, name='vendor_dashboard'),
    path('<slug:slug_txt>/pricing', views.pricing, name='vendor_pricing'),
    path('pricing/add_pricing', views.add_pricing, name='add_pricing'),
    path('edit_pricing/<int:price_id>', views.edit_pricing, name='edit_pricing'),
    path('delete_pricing/<int:price_id>', views.delete_pricing, name='delete_pricing'),
    path('<slug:slug_txt>/gallery', views.gallery, name='vendor_gallery'),
]



