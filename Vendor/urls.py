from django.urls import path
from . import views
urlpatterns = [
    path('<slug:slug_txt>', views.dashboard, name='vendor_dashboard'),
    path('<slug:slug_txt>/chats', views.chats, name='vendor_chats'),
    path('<slug:slug_txt>/notifications', views.notification, name='vendor_notifications'),
    path('vendor_chats/<slug:slug_txt>', views.vendor_user_chat, name='vendor_user_chat'),
    path('vendor_chats/send_message/<slug:slug_txt>', views.vendor_user_send_msg, name='vendor_user_send_msg'),
    path('<slug:slug_txt>/pricing', views.pricing, name='vendor_pricing'),
    path('pricing/add_pricing', views.add_pricing, name='add_pricing'),
    path('edit_pricing/<int:price_id>', views.edit_pricing, name='edit_pricing'),
    path('delete_pricing/<int:price_id>', views.delete_pricing, name='delete_pricing'),
    path('<slug:slug_txt>/gallery', views.gallery, name='vendor_gallery'),
    path('gallery/update_logo', views.update_logo, name='update_logo'),
    path('gallery/add_image', views.add_image, name='vendor_add_image'),
    path('delete_image/<int:img_id>', views.delete_image, name='vendor_delete_image'),
    path('<slug:slug_txt>/account', views.account, name='vendor_account'),
    path('edit_profile/', views.edit_profile, name='vendor_edit_profile'),
    path('edit_password/', views.edit_password, name='vendor_edit_password'),
    path('<slug:slug_txt>/ratings', views.ratings, name='vendor_ratings'),
    path('<slug:slug_txt>/reviews', views.reviews, name='vendor_reviews'),
    path('<slug:slug_txt>/appointments', views.appointments, name='vendor_appointments'),
    path('approve_appointment/<int:app_id>', views.approve_appointment, name='vendor_approve_appointment'),
    path('decline_appointment/<int:app_id>', views.decline_appointment, name='vendor_decline_appointment'),
    path('<slug:slug_txt>/bookings', views.bookings, name='vendor_bookings'),
    path('approve_booking/<int:b_id>', views.approve_booking, name='vendor_approve_booking'),
    path('decline_booking/<int:b_id>', views.decline_booking, name='vendor_decline_booking'),
]



