from django.urls import path
from . import views
urlpatterns = [
    path('<slug:slug_txt>', views.home, name='users_home'),
    path('users_search/<int:id>', views.users_search, name='users_search'),
    path('<slug:slug_txt>/vendors', views.users_vendors, name='users_vendors'),
    path('<slug:slug_txt>/chats', views.users_chats, name='users_chats'),
    path('<slug:slug_txt>/account', views.users_account, name='users_account'),
    path('<slug:slug_txt>/upload_image', views.upload_image, name='users_upload_image'),
    path('<slug:slug_txt>/upload_video', views.upload_video, name='users_upload_video'),
    path('edit_profile/', views.users_edit_profile, name='users_edit_profile'),
    path('edit_password/', views.users_edit_password, name='users_edit_password'),
    path('<slug:slug_txt>/check_list', views.check_list, name='users_check_list'),
    path('<slug:slug_txt>/budget', views.budget, name='users_budget'),
    path('<slug:slug_txt>/save_budget', views.save_budget, name='users_save_budget'),
    path('<slug:slug_txt>/all_b', views.get_all_budget, name='users_all_budgets'),
    path('<slug:slug_txt>/edit_check_list', views.edit_check_list, name='edit_users_check_list'),
    path('<slug:slug_txt>/gallery', views.gallery, name='users_gallery'),
    path('<slug:slug_txt>/upload', views.upload, name='users_upload'),
    path('delete_image/<int:img_id>', views.delete_image, name='users_delete_image'),
    path('delete_vid/<int:vid_id>', views.delete_vid, name='users_delete_vid'),
    path('user_chats/<slug:slug_txt>', views.user_vendor_chat, name='user_vendor_chat'),
    path('user_chats/send_message/<slug:slug_txt>', views.user_vendor_send_msg, name='user_vendor_send_msg'),
    path('users_vendor/<slug:slug_txt>', views.users_vendor, name='users_vendor'),
    path('rate_vendor/<slug:slug_txt>', views.rate_vendor, name='users_rate_vendor'),
    path('<slug:slug_txt>/make_appointment', views.make_appointment, name='users_make_appointment'),
    path('<slug:slug_txt>/make_booking', views.make_booking, name='users_make_booking'),
    path('send_message_vendor/<slug:slug_txt>', views.send_message, name='users_send_message_vendor'),
    path('update_vendor_rating/<int:rating_id>', views.update_rate_vendor, name='update_vendor_rating'),
    path('review_vendor/<slug:slug_txt>', views.review_vendor, name='users_review_vendor'),
    path('update_vendor_review/<int:review_id>', views.update_review_vendor, name='update_vendor_review'), \
    path('<slug:slug_txt>/appointments', views.appointments, name='users_appointments'),
    path('<slug:slug_txt>/bookings', views.bookings, name='users_bookings'),
    path('appointments/cancel/<int:ap_id>', views.cancel_appointment, name='users_cancel_appointment'),
    path('bookings/cancel/<int:bk_id>', views.cancel_booking, name='users_cancel_booking'),
    path('<slug:slug_txt>/notifications', views.notification, name='users_notifications'),

]


